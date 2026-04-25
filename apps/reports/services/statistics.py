from collections import defaultdict

from apps.reports.models import Report, ReportStatus


STATUS_LABELS = {
    "pending": {"uz": "Kutilmoqda", "en": "Pending", "ru": "В ожидании"},
    "accepted": {"uz": "Qabul qilingan", "en": "Accepted", "ru": "Принято"},
    "rejected": {"uz": "Rad etilgan", "en": "Rejected", "ru": "Отклонено"},
    "done": {"uz": "Yakunlangan", "en": "Done", "ru": "Завершено"},
}


def _pick_lang(language: str) -> str:
    language = (language or "uz").lower()
    if language.startswith("ru"):
        return "ru"
    if language.startswith("en"):
        return "en"
    return "uz"


def _pretty_name(identifier: str) -> str:
    text = (identifier or "").replace("-", " ").replace("_", " ").strip()
    return text.title() if text else "Unknown"


def build_statistics(language: str = "uz") -> dict:
    lang = _pick_lang(language)
    reports = list(Report.objects.all().order_by("-created_at"))

    totals = {
        "reports": len(reports),
        "accepted": sum(1 for report in reports if report.status == ReportStatus.ACCEPTED),
        "done": sum(1 for report in reports if report.status == ReportStatus.DONE),
        "pending": sum(1 for report in reports if report.status == ReportStatus.PENDING),
    }

    region_counter: dict[str, int] = defaultdict(int)
    organization_counter: dict[str, int] = defaultdict(int)
    city_counter: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    city_org_counter: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for report in reports:
        region_counter[report.region_id] += 1
        organization_counter[report.organization_id] += 1
        city_counter[report.region_id][report.city_id] += 1
        city_org_counter[(report.region_id, report.city_id)][report.organization_id] += 1

    by_region = [
        {"id": region_id, "name": _pretty_name(region_id), "count": count}
        for region_id, count in region_counter.items()
    ]
    by_region.sort(key=lambda item: (-item["count"], item["name"]))

    status_distribution = []
    for status in ReportStatus.values:
        status_distribution.append(
            {
                "id": status,
                "name": STATUS_LABELS[status][lang],
                "value": sum(1 for report in reports if report.status == status),
            }
        )

    top_organizations = [
        {
            "id": organization_id,
            "name": _pretty_name(organization_id),
            "count": count,
        }
        for organization_id, count in organization_counter.items()
    ]
    top_organizations.sort(key=lambda item: (-item["count"], item["name"]))
    top_organizations = top_organizations[:8]

    drilldown = {}
    for region_id, count in region_counter.items():
        cities = []
        for city_id, city_count in city_counter[region_id].items():
            organizations = [
                {
                    "id": organization_id,
                    "name": _pretty_name(organization_id),
                    "count": org_count,
                }
                for organization_id, org_count in city_org_counter[(region_id, city_id)].items()
            ]
            organizations.sort(key=lambda item: (-item["count"], item["name"]))
            cities.append(
                {
                    "id": city_id,
                    "name": _pretty_name(city_id),
                    "count": city_count,
                    "organizations": organizations,
                }
            )
        cities.sort(key=lambda item: (-item["count"], item["name"]))
        drilldown[region_id] = {
            "regionName": _pretty_name(region_id),
            "total": count,
            "cities": cities,
        }

    hotspot_regions = [
        {"id": item["id"], "name": item["name"], "count": item["count"]}
        for item in by_region
        if item["count"] > 0
    ][:3]

    return {
        "totals": totals,
        "byRegion": by_region,
        "statusDistribution": status_distribution,
        "topOrganizations": top_organizations,
        "drilldown": drilldown,
        "hotspotRegions": hotspot_regions,
    }
