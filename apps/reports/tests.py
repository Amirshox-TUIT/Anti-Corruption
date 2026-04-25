from rest_framework.test import APITestCase


class ReportApiTests(APITestCase):
    def test_report_lifecycle(self):
        payload = {
            "corruptionType": "bribery",
            "description": (
                "A municipal clerk repeatedly requested unofficial payment "
                "before releasing mandatory approval paperwork."
            ),
            "incidentDate": "2026-04-20",
            "regionId": "tashkent",
            "cityId": "tashkent-city",
            "organizationTypeId": "government-office",
            "organizationId": "tashkent-cadastre",
            "contact": "",
        }

        created = self.client.post("/api/reports", payload, format="json")
        self.assertEqual(created.status_code, 201)
        self.assertIn("trackingId", created.data["data"])
        self.assertEqual(created.data["data"]["status"], "pending")

        tracking_id = created.data["data"]["trackingId"]
        fetched = self.client.get(f"/api/reports/{tracking_id}")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(fetched.data["data"]["trackingId"], tracking_id)

    def test_admin_login_and_status_update(self):
        created = self.client.post(
            "/api/reports",
            {
                "corruptionType": "procurement",
                "description": (
                    "Vendor selection was manipulated and compliant bids were "
                    "ignored in exchange for private benefit."
                ),
                "incidentDate": "2026-04-21",
                "regionId": "samarkand",
                "cityId": "samarkand-city",
                "organizationTypeId": "hospital",
                "organizationId": "samarkand-regional-hospital",
            },
            format="json",
        )
        report_id = created.data["data"]["id"]

        login = self.client.post(
            "/api/admin/login",
            {"email": "inspector@anticor.uz", "password": "SecureAdmin123!"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        token = login.data["data"]["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        updated = self.client.patch(
            f"/api/admin/reports/{report_id}",
            {"status": "done"},
            format="json",
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data["data"]["status"], "done")
