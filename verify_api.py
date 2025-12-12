
import unittest
import json
import os
import shutil
from src.alertsAPI import AlertService
from src.config import OUTPUT_ALERTS_DIR

class TestAlertAPI(unittest.TestCase):
    def setUp(self):
        # Ensure directory exists
        if not os.path.exists(OUTPUT_ALERTS_DIR):
            os.makedirs(OUTPUT_ALERTS_DIR)
        
        # Create dummy alerts.json
        self.dummy_data = [{"id": 1, "timestamp": 123456}]
        with open(f"{OUTPUT_ALERTS_DIR}/alerts.json", "w") as f:
            json.dump(self.dummy_data, f)
            
        self.service = AlertService()
        self.app = self.service.app.test_client()

    def test_get_alerts_file(self):
        # Test direct method if possible, or via route
        response = self.app.get('/alerts/file')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('alerts', data)
        self.assertEqual(data['alerts'], self.dummy_data)

    def tearDown(self):
        # Cleanup
        if os.path.exists(f"{OUTPUT_ALERTS_DIR}/alerts.json"):
            os.remove(f"{OUTPUT_ALERTS_DIR}/alerts.json")

if __name__ == '__main__':
    unittest.main()
