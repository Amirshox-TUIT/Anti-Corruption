import re
import secrets
from typing import ClassVar

from django.db import models
from django.utils import timezone

from apps.shared.models import BaseModel


class CorruptionType(models.TextChoices):
    BRIBERY = "bribery", "Bribery"
    EMBEZZLEMENT = "embezzlement", "Embezzlement"
    ABUSE_OF_POWER = "abuse-of-power", "Abuse of power"
    PROCUREMENT = "procurement", "Procurement"
    EXTORTION = "extortion", "Extortion"
    OTHER = "other", "Other"


class ReportStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"
    DONE = "done", "Done"


TIMELINE_KEYS = {
    ReportStatus.PENDING: (
        "status.timeline.pending.title",
        "status.timeline.pending.description",
    ),
    ReportStatus.ACCEPTED: (
        "status.timeline.accepted.title",
        "status.timeline.accepted.description",
    ),
    ReportStatus.REJECTED: (
        "status.timeline.rejected.title",
        "status.timeline.rejected.description",
    ),
    ReportStatus.DONE: (
        "status.timeline.done.title",
        "status.timeline.done.description",
    ),
}


class Report(BaseModel):
    ALPHABET: ClassVar[str] = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    public_id = models.CharField(max_length=24, unique=True, db_index=True, editable=False)
    tracking_id = models.CharField(max_length=32, unique=True, db_index=True, editable=False)

    corruption_type = models.CharField(max_length=32, choices=CorruptionType.choices)
    description = models.TextField()
    incident_date = models.DateField()

    region_id = models.CharField(max_length=64)
    city_id = models.CharField(max_length=64)
    organization_type_id = models.CharField(max_length=64)
    organization_id = models.CharField(max_length=128)
    contact = models.CharField(max_length=255, blank=True, default="")

    status = models.CharField(
        max_length=16,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        db_index=True,
    )

    ai_summary = models.TextField(blank=True, default="")
    ai_risk_score = models.PositiveSmallIntegerField(null=True, blank=True)
    ai_flags = models.JSONField(default=list, blank=True)
    ai_source = models.CharField(max_length=24, blank=True, default="")

    class Meta:
        db_table = "reports"
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["region_id", "status"]),
            models.Index(fields=["tracking_id"]),
            models.Index(fields=["public_id"]),
        ]

    @classmethod
    def _build_public_id(cls) -> str:
        return f"REP-{secrets.randbelow(900000) + 100000}"

    @classmethod
    def _build_tracking_id(cls, region_id: str) -> str:
        region_code = re.sub(r"[^A-Za-z0-9]", "", region_id or "GEN").upper()[:3]
        region_code = (region_code + "XXX")[:3]
        random_tail = "".join(secrets.choice(cls.ALPHABET) for _ in range(4))
        year = timezone.now().strftime("%y")
        return f"UZ-{year}-{region_code}-{random_tail}"

    def save(self, *args, **kwargs):
        if not self.public_id:
            while True:
                candidate = self._build_public_id()
                if not Report.objects.filter(public_id=candidate).exists():
                    self.public_id = candidate
                    break

        if not self.tracking_id:
            while True:
                candidate = self._build_tracking_id(self.region_id)
                if not Report.objects.filter(tracking_id=candidate).exists():
                    self.tracking_id = candidate
                    break

        super().save(*args, **kwargs)

    def append_timeline(self, status: str) -> "ReportTimeline":
        title_key, description_key = TIMELINE_KEYS[status]
        return ReportTimeline.objects.create(
            report=self,
            status=status,
            title_key=title_key,
            description_key=description_key,
        )

    def __str__(self):
        return self.tracking_id


class ReportTimeline(BaseModel):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="timeline_entries",
    )
    status = models.CharField(max_length=16, choices=ReportStatus.choices)
    title_key = models.CharField(max_length=120)
    description_key = models.CharField(max_length=120)

    class Meta:
        db_table = "report_timelines"
        indexes = [models.Index(fields=["report", "created_at"])]

    def __str__(self):
        return f"{self.report.tracking_id} - {self.status}"


class ReportEvidence(BaseModel):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="evidence_items",
    )
    file = models.FileField(upload_to="reports/evidence/%Y/%m/%d/")
    original_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "report_evidences"
        indexes = [
            models.Index(fields=["report", "created_at"]),
        ]

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.original_name = self.original_name or self.file.name
            self.mime_type = getattr(self.file.file, "content_type", "") or "application/octet-stream"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report.tracking_id} - {self.original_name}"
