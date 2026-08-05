import os
import time
import json
import joblib
import numpy as np
import pandas as pd

class HealthPredictor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        models_dir = os.path.join(base_dir, 'backend', 'ml_engine', 'models')
        
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
        self.lr_model = joblib.load(os.path.join(models_dir, 'logistic_regression.joblib'))
        self.dt_model = joblib.load(os.path.join(models_dir, 'decision_tree.joblib'))
        self.rf_model = joblib.load(os.path.join(models_dir, 'random_forest.joblib'))
        
        with open(os.path.join(models_dir, 'metrics.json'), 'r') as f:
            self.metrics = json.load(f)
            
        self.feature_names = [
            'age', 'gender_code', 'systolic_bp', 'diastolic_bp', 
            'bmi', 'glucose_level', 'cholesterol', 
            'smoking_status', 'physical_activity', 'heart_rate', 'family_history'
        ]

    def predict(self, patient_data, model_name='random_forest'):
        start_time = time.time()
        
        gender_code = 1 if str(patient_data.get('gender')).lower() == 'male' else 0
        
        raw_dict = {
            'age': [float(patient_data.get('age', 40))],
            'gender_code': [gender_code],
            'systolic_bp': [float(patient_data.get('systolic_bp', 120))],
            'diastolic_bp': [float(patient_data.get('diastolic_bp', 80))],
            'bmi': [float(patient_data.get('bmi', 24.5))],
            'glucose_level': [float(patient_data.get('glucose_level', 95))],
            'cholesterol': [float(patient_data.get('cholesterol', 180))],
            'smoking_status': [int(patient_data.get('smoking_status', 0))],
            'physical_activity': [int(patient_data.get('physical_activity', 1))],
            'heart_rate': [float(patient_data.get('heart_rate', 72))],
            'family_history': [int(patient_data.get('family_history', 0))]
        }
        
        X_df = pd.DataFrame(raw_dict, columns=self.feature_names)
        X_scaled = self.scaler.transform(X_df)
        
        if model_name == 'logistic_regression':
            model = self.lr_model
        elif model_name == 'decision_tree':
            model = self.dt_model
        else:
            model = self.rf_model
            model_name = 'random_forest'
            
        probs = model.predict_proba(X_scaled)[0]
        pred_class = int(model.predict(X_scaled)[0])
        
        risk_labels = ['Low Risk', 'Moderate Risk', 'High Risk']
        risk_level = risk_labels[pred_class]
        overall_risk_score = float(probs[2] * 0.85 + probs[1] * 0.45 + probs[0] * 0.1)
        
        sys_bp = raw_dict['systolic_bp'][0]
        dia_bp = raw_dict['diastolic_bp'][0]
        bmi = raw_dict['bmi'][0]
        glucose = raw_dict['glucose_level'][0]
        chol = raw_dict['cholesterol'][0]
        smoking = raw_dict['smoking_status'][0]
        
        cardio_risk = 1 if (sys_bp > 135 or chol > 220 or overall_risk_score > 0.55) else 0
        diabetes_risk = 1 if (glucose > 125 or bmi > 30.0 or overall_risk_score > 0.50) else 0
        kidney_risk = 1 if (sys_bp > 140 and glucose > 135) else 0
        
        cardio_prob = float(min(max((sys_bp/180.0)*0.5 + (chol/300.0)*0.4 + (smoking*0.1), 0.1), 0.98))
        diabetes_prob = float(min(max((glucose/240.0)*0.6 + (bmi/40.0)*0.3, 0.08), 0.96))
        kidney_prob = float(min(max((sys_bp/190.0)*0.45 + (glucose/250.0)*0.45, 0.05), 0.92))
        
        key_factors = []
        if sys_bp >= 130:
            key_factors.append(f"Elevated Blood Pressure ({int(sys_bp)}/{int(dia_bp)} mmHg)")
        if bmi >= 25.0:
            key_factors.append(f"Overweight / Elevated BMI ({bmi} kg/m²)")
        if glucose >= 110:
            key_factors.append(f"Elevated Blood Glucose ({int(glucose)} mg/dL)")
        if chol >= 200:
            key_factors.append(f"High Total Cholesterol ({int(chol)} mg/dL)")
        if smoking > 0:
            key_factors.append("Tobacco Use / Smoking History")
        if raw_dict['family_history'][0] == 1:
            key_factors.append("Genetic / Family Medical History")
            
        if not key_factors:
            key_factors.append("Vital metrics within optimal reference ranges")
            
        recommendations = []
        if pred_class == 2:
            recommendations.append("Schedule an immediate comprehensive clinical health evaluation.")
            recommendations.append("Adopt low-sodium, heart-healthy dietary plan (DASH protocol).")
            recommendations.append("Monitor blood pressure and glucose daily.")
        elif pred_class == 1:
            recommendations.append("Increase moderate aerobic physical activity to 150+ mins/week.")
            recommendations.append("Reduce refined sugar and saturated fat intake.")
            recommendations.append("Schedule a routine annual preventive screening.")
        else:
            recommendations.append("Maintain current healthy dietary and physical activity routine.")
            recommendations.append("Continue regular wellness checkups.")
            
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            'risk_level': risk_level,
            'pred_class': pred_class,
            'overall_risk_score': round(overall_risk_score, 4),
            'probabilities': {
                'low_risk': round(float(probs[0]), 4),
                'moderate_risk': round(float(probs[1]), 4),
                'high_risk': round(float(probs[2]), 4)
            },
            'disease_risks': {
                'cardiovascular': {'flag': cardio_risk, 'probability': round(cardio_prob, 4)},
                'diabetes': {'flag': diabetes_risk, 'probability': round(diabetes_prob, 4)},
                'kidney': {'flag': kidney_risk, 'probability': round(kidney_prob, 4)}
            },
            'key_factors': key_factors,
            'recommendations': recommendations,
            'model_used': model_name,
            'latency_ms': latency_ms,
            'meets_sla': latency_ms < 1500.0
        }

if __name__ == '__main__':
    predictor = HealthPredictor()
    sample = {
        'age': 55, 'gender': 'Male', 'systolic_bp': 145, 'diastolic_bp': 92,
        'bmi': 31.2, 'glucose_level': 140, 'cholesterol': 235,
        'smoking_status': 2, 'physical_activity': 0, 'heart_rate': 84, 'family_history': 1
    }
    res = predictor.predict(sample)
    print("Sample Prediction Result:")
    print(json.dumps(res, indent=2))
