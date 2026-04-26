import os
import secrets
import uuid

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.reports.models import Report, ReportStatus
from apps.reports.serializers import (
    AdminCredentialsSerializer,
    ReportCreateSerializer,
    ReportReadSerializer,
    ReportStatusUpdateSerializer,
    RewardAssignSerializer,
    RewardClaimSerializer,
)
from apps.reports.services import build_report_ai_insight, build_statistics
from apps.shared.utils.custom_response import CustomResponse

User = get_user_model()



def _build_username(email: str) -> str:
    base = email.split("@")[0].replace(".", "_")[:20] or "admin"
    candidate = base
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}_{secrets.randbelow(9999):04d}"
    return candidate


def _bootstrap_default_admin(email: str, password: str):
    default_email = os.getenv("DEFAULT_ADMIN_EMAIL", "inspector@anticor.uz").strip().lower()
    default_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "SecureAdmin123!")

    if email.lower() != default_email or password != default_password:
        return

    user = User.objects.filter(email__iexact=default_email).first()
    if not user:
        user = User.objects.create_user(
            username=_build_username(default_email),
            email=default_email,
            password=default_password,
            first_name="Senior",
            last_name="Compliance Officer",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        return

    update_fields = []
    if not user.is_staff:
        user.is_staff = True
        update_fields.append("is_staff")
    if not user.is_superuser:
        user.is_superuser = True
        update_fields.append("is_superuser")
    if not user.is_active:
        user.is_active = True
        update_fields.append("is_active")
    if not user.check_password(default_password):
        user.set_password(default_password)
        update_fields.append("password")

    if update_fields:
        user.save(update_fields=update_fields)


def _simulate_crypto_payout(wallet: str, amount) -> str:
    """
    Demo / hackathon mode: generate a realistic-looking mock tx hash.
    Replace this with a real Web3 / exchange API call in production.
    """
    return "0x" + uuid.uuid4().hex + uuid.uuid4().hex[:24]


class ReportCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        payload = request.data.copy()
        if hasattr(payload, "setlist"):
            payload.setlist("evidenceFiles", request.FILES.getlist("evidenceFiles"))

        serializer = ReportCreateSerializer(data=payload)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request,
            )

        report = serializer.save()

        insight = build_report_ai_insight(
            description=report.description,
            corruption_type=report.corruption_type,
        )
        report.ai_summary = insight.summary
        report.ai_risk_score = insight.risk_score
        report.ai_flags = insight.flags
        report.ai_source = insight.source
        report.save(update_fields=["ai_summary", "ai_risk_score", "ai_flags", "ai_source", "updated_at"])

        data = ReportReadSerializer(report, context={"request": request}).data
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=data,
        )


class ReportRetrieveAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, tracking_id: str):
        report = (
            Report.objects.select_related()
            .prefetch_related("evidence_items", "timeline_entries")
            .filter(tracking_id__iexact=tracking_id)
            .first()
        )

        if not report:
            return CustomResponse.not_found(request=request, message_key="NOT_FOUND")

        data = ReportReadSerializer(report, context={"request": request}).data
        return CustomResponse.success(request=request, data=data)


class StatisticsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        language = request.query_params.get("language") or request.headers.get("Accept-Language", "uz")
        stats = build_statistics(language=language)
        return CustomResponse.success(request=request, data=stats)


class RewardClaimAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RewardClaimSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request,
            )

        report: Report = serializer.validated_data["report"]
        wallet: str = serializer.validated_data["wallet"]
        tx_hash = _simulate_crypto_payout(wallet, report.reward_amount)

        report.reward_claimed = True
        report.reward_wallet = wallet
        report.reward_claimed_at = timezone.now()
        report.reward_tx_hash = tx_hash
        report.save(
            update_fields=[
                "reward_claimed",
                "reward_wallet",
                "reward_claimed_at",
                "reward_tx_hash",
                "updated_at",
            ]
        )

        # Mask wallet for response
        if wallet.startswith("0x") and len(wallet) >= 10:
            masked = wallet[:6] + "****" + wallet[-4:]
        else:
            masked = wallet[:4] + "****" + wallet[-4:]

        return CustomResponse.success(
            message_key="REWARD_CLAIMED",
            request=request,
            data={
                "success": True,
                "sentTo": masked,
                "amount": str(report.reward_amount),
                "currency": "USDT",
                "txHash": tx_hash,
            },
        )


class AdminLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = str(request.data.get("password", ""))
        _bootstrap_default_admin(email=email, password=password)

        serializer = AdminCredentialsSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.unauthorized(
                message_key="INVALID_CREDENTIALS",
                request=request,
                errors=serializer.errors,
            )

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        payload = {
            "token": token.key,
            "email": user.email,
            "name": user.get_full_name().strip() or "Senior Compliance Officer",
        }
        return CustomResponse.success(
            message_key="LOGIN_SUCCESS",
            request=request,
            data=payload,
        )


class AdminReportListAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        region_id = request.query_params.get("regionId", "").strip()
        status = request.query_params.get("status", "").strip()
        organization = request.query_params.get("organization", "").strip()

        queryset = Report.objects.prefetch_related("evidence_items", "timeline_entries").all()

        if region_id:
            queryset = queryset.filter(region_id=region_id)

        if status and status != "all":
            queryset = queryset.filter(status=status)

        if organization:
            queryset = queryset.filter(
                Q(organization_id__icontains=organization)
                | Q(description__icontains=organization)
                | Q(contact__icontains=organization)
            )

        queryset = queryset.order_by("-created_at")
        data = ReportReadSerializer(queryset, many=True, context={"request": request}).data
        return CustomResponse.success(request=request, data=data)


class AdminReportStatusUpdateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, report_id: str):
        report = (
            Report.objects.prefetch_related("evidence_items", "timeline_entries")
            .filter(public_id=report_id)
            .first()
        )
        if not report:
            return CustomResponse.not_found(request=request, message_key="NOT_FOUND")

        serializer = ReportStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors,
            )

        next_status = serializer.validated_data["status"]
        if report.status != next_status:
            report.status = next_status
            report.save(update_fields=["status", "updated_at"])
            report.append_timeline(next_status)

        data = ReportReadSerializer(report, context={"request": request}).data
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=data,
        )


class AdminRewardAssignAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, report_id: str):
        report = (
            Report.objects.prefetch_related("evidence_items", "timeline_entries")
            .filter(public_id=report_id)
            .first()
        )
        if not report:
            return CustomResponse.not_found(request=request, message_key="NOT_FOUND")

        if report.status != ReportStatus.DONE:
            return CustomResponse.validation_error(
                request=request,
                errors={"status": ["Reward can only be assigned after the report is marked as done."]},
            )

        if report.reward_claimed:
            return CustomResponse.validation_error(
                request=request,
                errors={"reward": ["This reward has already been claimed and cannot be changed."]},
            )

        serializer = RewardAssignSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                request=request,
                errors=serializer.errors,
            )

        report.reward_amount = serializer.validated_data["amount"]
        report.save(update_fields=["reward_amount", "updated_at"])

        data = ReportReadSerializer(report, context={"request": request}).data
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=data,
        )