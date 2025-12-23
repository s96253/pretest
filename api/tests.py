from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Order


class ImportOrderAPITests(APITestCase):
    def setUp(self):
        self.url = reverse("import_order")

    def test_import_order_success_creates_order(self):
        payload = {
            "token": "omni_pretest_token",
            "order_number": "T001",
            "total_price": 123,
        }
        resp = self.client.post(self.url, payload, format="json")
        self.assertIn(resp.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertTrue(Order.objects.filter(order_number="T001").exists())

    def test_import_order_invalid_token(self):
        payload = {
            "token": "wrong_token",
            "order_number": "T002",
            "total_price": 100,
        }
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Order.objects.filter(order_number="T002").exists())

    def test_import_order_missing_fields(self):
        resp = self.client.post(
            self.url,
            {"token": "omni_pretest_token"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
