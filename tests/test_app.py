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

    def test_09_input_validation_failure(self):
        """Verify Input Validation Rejects Invalid Vitals (HTTP 400)"""
        # Test Systolic <= Diastolic
        payload_bp = {
            'age': 45, 'gender': 'Male', 'height_cm': 175, 'weight_kg': 75,
            'systolic_bp': 110, 'diastolic_bp': 120, 'glucose': 95, 'cholesterol': 180
        }
        res = self.client.post('/api/predict', data=json.dumps(payload_bp), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Systolic BP must be greater than Diastolic BP.')

        # Test Out of Bounds Age
        payload_age = {
            'age': 150, 'gender': 'Male', 'height_cm': 175, 'weight_kg': 75,
            'systolic_bp': 130, 'diastolic_bp': 85, 'glucose': 95, 'cholesterol': 180
        }
        res = self.client.post('/api/predict', data=json.dumps(payload_age), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Age must be between 1 and 120 years.')

    def test_10_sorting_allowlist_fallback(self):
        """Verify Invalid Column Sort Parameters Fall Back Safely to Created At"""
        res = self.client.get('/api/patients?sort_by=invalid_column_name&order=asc')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['records']) > 0)

    def test_11_analytics_accurate_counts(self):
        """Verify Analytics API Returns Dictionary Breakdown Without Hardcoded Fallbacks"""
        res = self.client.get('/api/analytics')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('risk_breakdown', data)
        self.assertIn('Low', data['risk_breakdown'])
        self.assertIn('disease_prevalence', data)
        self.assertIn('heart_disease', data['disease_prevalence'])

    def test_12_feature_importance_and_security_headers(self):
        """Verify Feature Importance Engine & Enterprise Security Headers"""
        res = self.client.get('/api/health')
        self.assertEqual(res.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(res.headers.get('X-Frame-Options'), 'SAMEORIGIN')

        payload = {
            'patient_code': 'TEST-9900',
            'patient_name': 'Feature Importance Test',
            'age': 45, 'gender': 'Male', 'height_cm': 175, 'weight_kg': 78,
            'systolic_bp': 135, 'diastolic_bp': 88, 'glucose': 105, 'cholesterol': 195,
            'heart_rate': 74, 'smoking': 0, 'alcohol': 0, 'exercise': 1, 'family_history': 0
        }
        res_pred = self.client.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res_pred.status_code, 200)
        data = json.loads(res_pred.data)
        self.assertIn('feature_importance', data['data'])

if __name__ == '__main__':
    unittest.main()


