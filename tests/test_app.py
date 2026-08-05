import os
import sys
import json
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app import app
from ml.predictor import HealthPredictor

class TestMedPredictAI(unittest.TestCase):
    """Automated Enterprise Test Suite for MedPredict AI Platform"""
    
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_01_health_endpoint(self):
        """Verify API Health Check Endpoint"""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'healthy')

    def test_02_predict_endpoint_sla(self):
        """Verify Real-Time Risk Prediction SLA (< 1000 ms)"""
        payload = {
            'patient_code': 'TEST-8800',
            'patient_name': 'Automated Test Patient',
            'age': 52,
            'gender': 'Male',
            'height_cm': 176,
            'weight_kg': 84,
            'bmi': 27.1,
            'systolic_bp': 142,
            'diastolic_bp': 90,
            'glucose': 135,
            'cholesterol': 225,
            'heart_rate': 78,
            'smoking': 1,
            'alcohol': 1,
            'exercise': 1,
            'family_history': 1,
            'model_name': 'random_forest'
        }
        res = self.client.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['data']['latency_ms'] < 1000.0) # Sub-1-second SLA
        self.assertIn('disease_probs', data['data'])
        self.assertIn('heart_disease', data['data']['disease_probs'])

    def test_03_patients_history_log_sorting(self):
        """Verify Paginated Patient History Records & Sorting (500+ Records)"""
        res = self.client.get('/api/patients?page=1&per_page=10&sort_by=age&order=asc')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['total'], 500)
        self.assertTrue(len(data['records']) > 0)

    def test_04_system_status_telemetry(self):
        """Verify Live System Telemetry Endpoint"""
        res = self.client.get('/api/system/status')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('status', data)
        self.assertIn('database', data['status'])

    def test_05_analytics_endpoint(self):
        """Verify Population Health Analytics API"""
        res = self.client.get('/api/analytics')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('disease_prevalence', data)

    def test_06_models_metrics_endpoint(self):
        """Verify ML Benchmarking Metrics Endpoint"""
        res = self.client.get('/api/models/metrics')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('metrics', data)

    def test_07_reports_endpoint(self):
        """Verify Reports Counter & Audit Log Endpoint"""
        res = self.client.get('/api/reports')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['total_reports'], 1)

    def test_08_ml_predictor_standalone(self):
        """Verify ML Predictor Multi-Disease Engine Directly"""
        predictor = HealthPredictor()
        sample = {
            'age': 25, 'gender': 'Female', 'height_cm': 165, 'weight_kg': 58,
            'systolic_bp': 110, 'diastolic_bp': 70, 'glucose': 85, 'cholesterol': 160,
            'smoking': 0, 'alcohol': 0, 'exercise': 2, 'heart_rate': 65, 'family_history': 0
        }
        res = predictor.predict(sample, model_name='random_forest')
        self.assertEqual(res['risk_level'], 'Low')
        self.assertTrue(res['latency_ms'] < 1000.0)

if __name__ == '__main__':
    unittest.main()
