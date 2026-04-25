from django.contrib import admin

from apps.reports.models import Report, ReportEvidence, ReportTimeline


class ReportEvidenceInline(admin.TabularInline):
    model = ReportEvidence
    extra = 0


class ReportTimelineInline(admin.TabularInline):
    model = ReportTimeline
    extra = 0
    readonly_fields = ("status", "title_key", "description_key", "created_at")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("public_id", "tracking_id", "corruption_type", "status", "region_id", "created_at")
    list_filter = ("status", "corruption_type", "region_id")
    search_fields = ("public_id", "tracking_id", "description", "organization_id", "contact")
    readonly_fields = ("public_id", "tracking_id", "created_at", "updated_at")
    inlines = [ReportEvidenceInline, ReportTimelineInline]
