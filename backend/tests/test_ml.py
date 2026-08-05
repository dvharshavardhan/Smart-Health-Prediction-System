import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from backend.ml_engine.predictor import HealthPredictor

class TestMLEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.predictor = HealthPredictor()

    def test_predictor_healthy_patient(self):
        sample = {
            'age': 25, 'gender': 'Female', 'systolic_bp': 110, 'diastolic_bp': 70,
            'bmi': 21.0, 'glucose_level': 85, 'cholesterol': 160,
            'smoking_status': 0, 'physical_activity': 2, 'heart_rate': 65, 'family_history': 0
        }
        res = self.predictor.predict(sample, model_name='random_forest')
        self.assertEqual(res['risk_level'], 'Low Risk')
        self.assertTrue(res['latency_ms'] < 1500.0) # SLA requirement

    def test_predictor_high_risk_patient(self):
        sample = {
            'age': 65, 'gender': 'Male', 'systolic_bp': 165, 'diastolic_bp': 98,
            'bmi': 34.5, 'glucose_level': 180, 'cholesterol': 275,
            'smoking_status': 2, 'physical_activity': 0, 'heart_rate': 92, 'family_history': 1
        }
        res = self.predictor.predict(sample, model_name='random_forest')
        self.assertEqual(res['risk_level'], 'High Risk')
        self.assertTrue(res['overall_risk_score'] > 0.50)

    def test_all_models(self):
        sample = {
            'age': 45, 'gender': 'Male', 'systolic_bp': 130, 'diastolic_bp': 85,
            'bmi': 26.5, 'glucose_level': 105, 'cholesterol': 195,
            'smoking_status': 0, 'physical_activity': 1, 'heart_rate': 72, 'family_history': 0
        }
        for model in ['random_forest', 'logistic_regression', 'decision_tree']:
            res = self.predictor.predict(sample, model_name=model)
            self.assertIn(res['risk_level'], ['Low Risk', 'Moderate Risk', 'High Risk'])

if __name__ == '__main__':
    unittest.main()
