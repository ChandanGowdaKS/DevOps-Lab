import unittest
import json
from app import app

class TestOrderAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_root_endpoint(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["app"], "Order Management Service")

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(data["health"], "UP")

    def test_orders_list(self):
        res = self.client.get("/api/v1/orders")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(data["orders_count"], 2)

if __name__ == "__main__":
    unittest.main()
