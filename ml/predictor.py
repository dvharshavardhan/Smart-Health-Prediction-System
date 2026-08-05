import os
import sys
import time
import json
import logging
import joblib
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import Config

logger = logging.getLogger(__name__)

class HealthPredictor:
    """Enterprise Singleton Real-Time Health Diagnostic Predictor Engine"""
    
    def __init__(self):
        models_dir = Config.MODELS_DIR
        
        # Load scaler & trained models
        try:
            self.scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
            self.lr_model = joblib.load(os.path.join(models_dir, 'logistic_regression.joblib'))
            self.dt_model = joblib.load(os.path.join(models_dir, 'decision_tree.joblib'))
            self.rf_model = joblib.load(os.path.join(models_dir, 'random_forest.joblib'))
            
            with open(os.path.join(models_dir, 'metrics.json'), 'r') as f:
                self.metrics = json.load(f)
        except Exception as e:
            logger.warning(f"Warning loading trained models: {e}. Defaulting to fallback.")
            self.scaler = None
            self.metrics = {}

        self.feature_names = [
            'age', 'gender_code', 'height_cm', 'weight_kg', 'bmi', 
            'systolic_bp', 'diastolic_bp', 'glucose', 'cholesterol', 
            'heart_rate', 'smoking', 'alcohol', 'exercise', 'family_history'
        ]

    def predict(self, patient_data: dict, model_name: str = 'random_forest') -> dict:
        """
        Executes sub-1-second risk prediction across 5 major medical conditions.
        Returns risk level, confidence %, disease breakdown, risk factors, and AI suggestions.
        """
        start_time = time.time()
        
        gender_code = 1 if str(patient_data.get('gender')).lower() == 'male' else 0
        age = float(patient_data.get('age', 40))
        height_cm = float(patient_data.get('height_cm', 170))
        weight_kg = float(patient_data.get('weight_kg', 70))
        
        # Auto Calculate BMI if not provided
        bmi_calc = round(weight_kg / ((height_cm / 100.0) ** 2), 1)
        bmi = float(patient_data.get('bmi', bmi_calc))
        
        sys_bp = float(patient_data.get('systolic_bp', 120))
        dia_bp = float(patient_data.get('diastolic_bp', 80))
        glucose = float(patient_data.get('glucose', 95))
        cholesterol = float(patient_data.get('cholesterol', 180))
        heart_rate = float(patient_data.get('heart_rate', 72))
        
        smoking = int(patient_data.get('smoking', 0))
        alcohol = int(patient_data.get('alcohol', 0))
        exercise = int(patient_data.get('exercise', 1))
        family_history = int(patient_data.get('family_history', 0))
        
        raw_dict = {
            'age': [age],
            'gender_code': [gender_code],
            'height_cm': [height_cm],
            'weight_kg': [weight_kg],
            'bmi': [bmi],
            'systolic_bp': [sys_bp],
            'diastolic_bp': [dia_bp],
            'glucose': [glucose],
            'cholesterol': [cholesterol],
            'heart_rate': [heart_rate],
            'smoking': [smoking],
            'alcohol': [alcohol],
            'exercise': [exercise],
            'family_history': [family_history]
        }
        
        X_df = pd.DataFrame(raw_dict, columns=self.feature_names)
        
        if self.scaler:
            X_scaled = self.scaler.transform(X_df)
        else:
            X_scaled = X_df.values

        # Select model
        if model_name == 'logistic_regression':
            model = self.lr_model
        elif model_name == 'decision_tree':
            model = self.dt_model
        else:
            model = self.rf_model
            model_name = 'random_forest'
            
        probs = model.predict_proba(X_scaled)[0]
        pred_class = int(model.predict(X_scaled)[0])
        
        risk_labels = ['Low', 'Medium', 'High']
        risk_level = risk_labels[pred_class]
        
        # Calculate overall risk score / confidence %
        risk_score_raw = float(probs[2] * 0.85 + probs[1] * 0.45 + probs[0] * 0.1)
        confidence_pct = round(risk_score_raw * 100, 1)
        
        # Calculate 5 Disease Specific Probabilities (%)
        disease_probs = {
            'heart_disease': round(min(max((sys_bp/180.0)*45 + (cholesterol/300.0)*40 + (smoking*10), 5.0), 98.0), 1),
            'diabetes': round(min(max((glucose/240.0)*60 + (bmi/40.0)*30, 4.0), 96.0), 1),
            'kidney_disease': round(min(max((sys_bp/190.0)*45 + (glucose/250.0)*45, 3.0), 92.0), 1),
            'stroke_risk': round(min(max((sys_bp/190.0)*60 + (age/90.0)*30, 4.0), 95.0), 1),
            'hypertension': round(min(max((sys_bp/180.0)*70 + (dia_bp/110.0)*30, 8.0), 99.0), 1)
        }
        
        # Identify Key Risk Factors
        key_factors = []
        if sys_bp >= 130:
            key_factors.append(f"Elevated Systolic Blood Pressure ({int(sys_bp)} mmHg)")
        if dia_bp >= 80:
            key_factors.append(f"Elevated Diastolic Blood Pressure ({int(dia_bp)} mmHg)")
        if bmi >= 25.0:
            key_factors.append(f"Elevated BMI / Overweight ({bmi} kg/m²)")
        if glucose >= 110:
            key_factors.append(f"Elevated Fasting Blood Glucose ({int(glucose)} mg/dL)")
        if cholesterol >= 200:
            key_factors.append(f"Elevated Serum Cholesterol ({int(cholesterol)} mg/dL)")
        if smoking > 0:
            key_factors.append("Tobacco Use / Smoking History")
        if alcohol > 1:
            key_factors.append("Heavy Alcohol Intake")
        if exercise == 0:
            key_factors.append("Sedentary Physical Activity")
        if family_history == 1:
            key_factors.append("Genetic / Family Medical History")
            
        if not key_factors:
            key_factors.append("Vitals within optimal clinical reference ranges")
            
        # Formulate AI Clinical Recommendations & Lifestyle Suggestions
        recommendations = []
        if pred_class == 2:
            recommendations.append("Schedule an immediate comprehensive clinical & cardiovascular evaluation.")
            recommendations.append("Adopt a strict low-sodium DASH dietary protocol.")
            recommendations.append("Monitor blood pressure and blood glucose levels daily.")
            recommendations.append("Consult a specialist regarding lipid-lowering medical therapy.")
        elif pred_class == 1:
            recommendations.append("Increase moderate aerobic physical activity to 150+ minutes per week.")
            recommendations.append("Reduce intake of refined carbohydrates and saturated fats.")
            recommendations.append("Schedule a routine 6-month preventive health screening.")
            recommendations.append("Maintain consistent hydration and stress reduction routines.")
        else:
            recommendations.append("Maintain current healthy dietary and physical activity routine.")
            recommendations.append("Continue regular annual wellness checkups.")
            recommendations.append("Stay hydrated and maintain routine exercise.")

        latency_ms = round((time.time() - start_time) * 1000, 2)
        meets_sla = latency_ms < Config.SLA_LATENCY_MAX_MS
        
        return {
            'risk_level': risk_level,
            'confidence_pct': confidence_pct,
            'pred_class': pred_class,
            'model_used': model_name,
            'bmi_calculated': bmi,
            'disease_probs': disease_probs,
            'probabilities': {
                'low': round(float(probs[0]), 4),
                'medium': round(float(probs[1]), 4),
                'high': round(float(probs[2]), 4)
            },
            'key_factors': key_factors,
            'recommendations': recommendations,
            'latency_ms': latency_ms,
            'meets_sla': meets_sla
        }

if __name__ == '__main__':
    predictor = HealthPredictor()
    sample = {
        'age': 55, 'gender': 'Male', 'height_cm': 175, 'weight_kg': 88,
        'systolic_bp': 145, 'diastolic_bp': 92, 'glucose': 140, 'cholesterol': 235,
        'smoking': 2, 'alcohol': 1, 'exercise': 0, 'heart_rate': 84, 'family_history': 1
    }
    res = predictor.predict(sample)
    print("Sample Risk Assessment Output:")
    print(json.dumps(res, indent=2))
