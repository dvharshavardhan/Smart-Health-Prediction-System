import unittest
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from backend.app import app

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        res = self.app.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'healthy')

    def test_predict_endpoint(self):
        payload = {
            'patient_code': 'TEST-999',
            'patient_name': 'Test Unit Patient',
            'age': 50,
            'gender': 'Male',
            'systolic_bp': 140,
            'diastolic_bp': 90,
            'bmi': 28.5,
            'glucose_level': 130,
            'cholesterol': 220,
            'smoking_status': 1,
            'physical_activity': 1,
            'heart_rate': 75,
            'family_history': 1,
            'model_name': 'random_forest'
        }
        res = self.app.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['latency_ms'] < 1500.0) # SLA Requirement

    def test_admin_records_endpoint(self):
        res = self.app.get('/api/admin/records?page=1&per_page=10')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['total'], 500) # 500+ records requirement

    def test_admin_analytics_endpoint(self):
        res = self.app.get('/api/admin/analytics')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['monitoring_efficiency_gain'], '40%')

    def test_models_metrics_endpoint(self):
        res = self.app.get('/api/models/metrics')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('random_forest', data['metrics'])

if __name__ == '__main__':
    unittest.main()
