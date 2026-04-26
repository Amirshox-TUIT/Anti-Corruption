import re

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import serializers

from apps.reports.models import CorruptionType, Report, ReportEvidence, ReportStatus

User = get_user_model()

# Basic crypto wallet validation (ETH / EVM compatible, Tron TRC-20, Solana)
_WALLET_RE = re.compile(
    r"^(0x[0-9a-fA-F]{40}"   # Ethereum / EVM
    r"|T[1-9A-HJ-NP-Za-km-z]{33}"  # Tron (USDT-TRC20)
    r"|[1-9A-HJ-NP-Za-km-z]{32,44}"  # Solana / Bitcoin base58
    r")$"
)


class ReportEvidenceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField(source="original_name")
    size = serializers.IntegerField(source="file_size")
    type = serializers.CharField(source="mime_type")
    previewUrl = serializers.SerializerMethodField()

    class Meta:
        model = ReportEvidence
        fields = ("id", "name", "size", "type", "previewUrl")

    def get_id(self, obj: ReportEvidence) -> str:
        return f"e-{obj.pk}"

    def get_previewUrl(self, obj: ReportEvidence) -> str:
        request = self.context.get("request")
        if not obj.file:
            return ""
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


class ReportTimelineSerializer(serializers.Serializer):
    status = serializers.CharField()
    date = serializers.DateTimeField(source="created_at")
    titleKey = serializers.CharField(source="title_key")
    descriptionKey = serializers.CharField(source="description_key")


class ReportReadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="public_id")
    trackingId = serializers.CharField(source="tracking_id")
    corruptionType = serializers.CharField(source="corruption_type")
    incidentDate = serializers.DateField(source="incident_date")
    regionId = serializers.CharField(source="region_id")
    cityId = serializers.CharField(source="city_id")
    organizationTypeId = serializers.CharField(source="organization_type_id")
    organizationId = serializers.CharField(source="organization_id")
    createdAt = serializers.DateTimeField(source="created_at")
    updatedAt = serializers.DateTimeField(source="updated_at")
    evidence = serializers.SerializerMethodField()
    timeline = serializers.SerializerMethodField()
    aiInsight = serializers.SerializerMethodField()
    rewardInfo = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "id",
            "trackingId",
            "corruptionType",
            "description",
            "incidentDate",
            "regionId",
            "cityId",
            "organizationTypeId",
            "organizationId",
            "contact",
            "status",
            "createdAt",
            "updatedAt",
            "evidence",
            "timeline",
            "aiInsight",
            "rewardInfo",
        )

    def get_evidence(self, obj: Report):
        serializer = ReportEvidenceSerializer(
            obj.evidence_items.all().order_by("created_at"),
            many=True,
            context=self.context,
        )
        return serializer.data

    def get_timeline(self, obj: Report):
        serializer = ReportTimelineSerializer(
            obj.timeline_entries.all().order_by("created_at"),
            many=True,
        )
        return serializer.data

    def get_aiInsight(self, obj: Report):
        if not obj.ai_summary and obj.ai_risk_score is None and not obj.ai_flags:
            return None
        return {
            "summary": obj.ai_summary,
            "riskScore": obj.ai_risk_score,
            "flags": obj.ai_flags,
            "source": obj.ai_source or "heuristic",
        }

    def get_rewardInfo(self, obj: Report):
        """
        Public-safe reward snapshot.
        Wallet address is masked after claim to protect anonymity:
          0xA1B2C3...DEAD  →  0xA1B2****DEAD
        """
        if obj.reward_amount is None:
            return None

        wallet = obj.reward_wallet or ""
        masked_wallet = ""
        if wallet:
            if wallet.startswith("0x") and len(wallet) >= 10:
                masked_wallet = wallet[:6] + "****" + wallet[-4:]
            else:
                masked_wallet = wallet[:4] + "****" + wallet[-4:]

        return {
            "amount": str(obj.reward_amount),
            "currency": "USDT",
            "claimed": obj.reward_claimed,
            "claimedAt": obj.reward_claimed_at,
            "wallet": masked_wallet,
            "txHash": obj.reward_tx_hash or None,
        }


class ReportCreateSerializer(serializers.Serializer):
    corruptionType = serializers.ChoiceField(choices=CorruptionType.choices)
    description = serializers.CharField(min_length=40)
    incidentDate = serializers.DateField()
    regionId = serializers.CharField(max_length=64)
    cityId = serializers.CharField(max_length=64)
    organizationTypeId = serializers.CharField(max_length=64)
    organizationId = serializers.CharField(max_length=128)
    evidenceFiles = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    def validate_incidentDate(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Incident date cannot be in the future.")
        return value

    def create(self, validated_data):
        files = validated_data.pop("evidenceFiles", [])
        report = Report.objects.create(
            corruption_type=validated_data["corruptionType"],
            description=validated_data["description"].strip(),
            incident_date=validated_data["incidentDate"],
            region_id=validated_data["regionId"],
            city_id=validated_data["cityId"],
            organization_type_id=validated_data["organizationTypeId"],
            organization_id=validated_data["organizationId"],
            contact=validated_data.get("contact", "").strip(),
        )
        report.append_timeline(ReportStatus.PENDING)

        for file_obj in files:
            ReportEvidence.objects.create(
                report=report,
                file=file_obj,
                original_name=file_obj.name,
                mime_type=getattr(file_obj, "content_type", "") or "application/octet-stream",
                file_size=getattr(file_obj, "size", 0) or 0,
            )

        return report


class ReportStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ReportStatus.choices)


class RewardAssignSerializer(serializers.Serializer):
    """Admin assigns a reward amount when marking a report as done."""

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value="1.00",
    )


class RewardClaimSerializer(serializers.Serializer):
    """
    Whistleblower submits tracking_id + wallet to claim reward.
    No authentication required — the tracking_id *is* the secret token.
    """

    trackingId = serializers.CharField()
    wallet = serializers.CharField(max_length=255)

    def validate_wallet(self, value: str) -> str:
        value = value.strip()
        if not _WALLET_RE.match(value):
            raise serializers.ValidationError(
                "Invalid wallet address. Supported formats: EVM (0x…), Tron (T…), Solana."
            )
        return value

    def validate(self, attrs):
        tracking_id = attrs["trackingId"].strip()
        report = (
            Report.objects.filter(tracking_id__iexact=tracking_id)
            .select_related()
            .first()
        )

        if not report:
            raise serializers.ValidationError({"trackingId": "No report found with this tracking ID."})

        if report.status != ReportStatus.DONE:
            raise serializers.ValidationError(
                {"trackingId": "Reward is only available after the report is marked as done."}
            )

        if report.reward_amount is None:
            raise serializers.ValidationError(
                {"trackingId": "No reward has been assigned to this report yet."}
            )

        if report.reward_claimed:
            raise serializers.ValidationError(
                {"trackingId": "This reward has already been claimed."}
            )

        attrs["report"] = report
        return attrs


class AdminCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        user = User.objects.filter(email__iexact=email).first()
        if user:
            authenticated = authenticate(username=user.get_username(), password=password)
            if not authenticated:
                raise serializers.ValidationError("Invalid credentials.")
            attrs["user"] = authenticated
            return attrs

        raise serializers.ValidationError("Invalid credentials.")