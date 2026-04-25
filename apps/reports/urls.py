from django.urls import path

from apps.reports.views import (
    AdminLoginAPIView,
    AdminReportListAPIView,
    AdminReportStatusUpdateAPIView,
    ReportCreateAPIView,
    ReportRetrieveAPIView,
    StatisticsAPIView,
)

urlpatterns = [
    path("reports", ReportCreateAPIView.as_view(), name="report-create"),
    path("reports/<str:tracking_id>", ReportRetrieveAPIView.as_view(), name="report-retrieve"),
    path("statistics", StatisticsAPIView.as_view(), name="statistics"),
    path("admin/login", AdminLoginAPIView.as_view(), name="admin-login"),
    path("admin/reports", AdminReportListAPIView.as_view(), name="admin-reports"),
    path("admin/reports/<str:report_id>", AdminReportStatusUpdateAPIView.as_view(), name="admin-report-update"),
]
