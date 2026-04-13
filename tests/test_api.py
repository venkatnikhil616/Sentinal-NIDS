import unittest
import json

from app.main import app


class TestAPI(unittest.TestCase):                       
    @classmethod
    def setUpClass(cls):
        """
        Setup Flask test client
        """
        app.testing = True                                
      cls.client = app.test_client()

        # Sample valid payload
        cls.sample_event = {                                    
            "duration": 1,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "SF",
            "src_bytes": 200,
            "dst_bytes": 1000,
            "wrong_fragment": 0,
            "urgent": 0,
            "hot": 0,
            "num_failed_logins": 0,
            "logged_in": 1,
            "num_compromised": 0,
            "root_shell": 0,
            "su_attempted": 0,
            "num_root": 0,
            "num_file_creations": 0,
            "num_shells": 0,
            "num_access_files": 0,
            "num_outbound_cmds": 0,
            "is_host_login": 0,
            "is_guest_login": 0,
            "count": 5,
            "srv_count": 5,
            "serror_rate": 0.0,
            "srv_serror_rate": 0.0,
            "rerror_rate": 0.0,
            "srv_rerror_rate": 0.0,
            "same_srv_rate": 1.0,
            "diff_srv_rate": 0.0,
            "srv_diff_host_rate": 0.0
        }

    # TEST HOME ROUTE

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # TEST DETECTION API
  
    def test_detection_api(self):
        response = self.client.post(
            "/detect",
            data=json.dumps(self.sample_event),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("attack_type", data)
        self.assertIn("confidence", data)

    # TEST INVALID PAYLOAD
  
    def test_invalid_payload(self):
        response = self.client.post(
            "/detect",
            data=json.dumps({"invalid": "data"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertTrue("error" in data or "attack_type" in data)

    # TEST DASHBOARD ROUTE

    def test_dashboard_route(self):
        response = self.client.get("/dashboard")

        # Some setups may redirect → allow 200 or 302
        self.assertIn(response.status_code, [200, 302])

    # TEST METHOD NOT ALLOWED

    def test_method_not_allowed(self):
        response = self.client.get("/detect")
        self.assertIn(response.status_code, [405, 404])


# RUN TESTS

if __name__ == "__main__":
    unittest.main()
