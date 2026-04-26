from django.urls import path

from apps.reports.views import (
    AdminLoginAPIView,
    AdminReportListAPIView,
    AdminReportStatusUpdateAPIView,
    AdminRewardAssignAPIView,
    ReportCreateAPIView,
    ReportRetrieveAPIView,
    RewardClaimAPIView,
    StatisticsAPIView,
)

urlpatterns = [
    path("reports/", ReportCreateAPIView.as_view(), name="report-create"),
    path("reports/<str:tracking_id>/", ReportRetrieveAPIView.as_view(), name="report-retrieve"),
    path("statistics/", StatisticsAPIView.as_view(), name="statistics"),
    path("rewards/claim/", RewardClaimAPIView.as_view(), name="reward-claim"),
    path("admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("admin/reports/", AdminReportListAPIView.as_view(), name="admin-report-list"),
    path("admin/reports/<str:report_id>/", AdminReportStatusUpdateAPIView.as_view(), name="admin-report-update"),
    path(
        "admin/reports/<str:report_id>/reward/",
        AdminRewardAssignAPIView.as_view(),
        name="admin-reward-assign",
    ),
]
