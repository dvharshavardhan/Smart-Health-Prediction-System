import json
from datetime import datetime
from database import db

class Patient(db.Model):
    """Demographic Records for Patients"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    predictions = db.relationship('Prediction', backref='patient', lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'patient_code': self.patient_code,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'bmi': self.bmi,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class Prediction(db.Model):
    """Clinical AI Risk Assessment Records"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    patient_code = db.Column(db.String(50), nullable=False, index=True)
    patient_name = db.Column(db.String(100), nullable=False)
    
    # Clinical Vitals
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height_cm = db.Column(db.Float, nullable=False, default=170.0)
    weight_kg = db.Column(db.Float, nullable=False, default=70.0)
    bmi = db.Column(db.Float, nullable=False)
    systolic_bp = db.Column(db.Float, nullable=False)
    diastolic_bp = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    
    # Lifestyle & Medical History
    smoking = db.Column(db.Integer, nullable=False, default=0) # 0: Never, 1: Former, 2: Current
    alcohol = db.Column(db.Integer, nullable=False, default=0) # 0: None, 1: Moderate, 2: Heavy
    exercise = db.Column(db.Integer, nullable=False, default=1) # 0: Low, 1: Moderate, 2: High
    family_history = db.Column(db.Integer, nullable=False, default=0) # 0: No, 1: Yes
    
    # AI Prediction Metrics
    model_used = db.Column(db.String(50), nullable=False)
    risk_level = db.Column(db.String(20), nullable=False, index=True) # 'Low', 'Medium', 'High'
    confidence_pct = db.Column(db.Float, nullable=False) # Probability %
    
    # Structured JSON Details
    disease_probs_json = db.Column(db.Text, nullable=False) # Heart, Diabetes, Kidney, Stroke, Hypertension
    recommendations_json = db.Column(db.Text, nullable=False)
    key_factors_json = db.Column(db.Text, nullable=False)
    
    # SLA & System Performance
    latency_ms = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_code': self.patient_code,
            'patient_name': self.patient_name,
            'age': self.age,
            'gender': self.gender,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'bmi': self.bmi,
            'systolic_bp': self.systolic_bp,
            'diastolic_bp': self.diastolic_bp,
            'glucose': self.glucose,
            'heart_rate': self.heart_rate,
            'cholesterol': self.cholesterol,
            'smoking': self.smoking,
            'alcohol': self.alcohol,
            'exercise': self.exercise,
            'family_history': self.family_history,
            'model_used': self.model_used,
            'risk_level': self.risk_level,
            'confidence_pct': self.confidence_pct,
            'disease_probs': json.loads(self.disease_probs_json) if self.disease_probs_json else {},
            'recommendations': json.loads(self.recommendations_json) if self.recommendations_json else [],
            'key_factors': json.loads(self.key_factors_json) if self.key_factors_json else [],
            'latency_ms': self.latency_ms,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class ModelMetric(db.Model):
    """ML Model Benchmarking Performance Tracking"""
    __tablename__ = 'model_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(50), unique=True, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)
    confusion_matrix_json = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'model_name': self.model_name,
            'accuracy': round(self.accuracy * 100, 2),
            'precision': round(self.precision * 100, 2),
            'recall': round(self.recall * 100, 2),
            'f1_score': round(self.f1_score * 100, 2),
            'confusion_matrix': json.loads(self.confusion_matrix_json) if self.confusion_matrix_json else []
        }

class ReportLog(db.Model):
    """Audit Trail for Generated Reports"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_code = db.Column(db.String(50), unique=True, nullable=False)
    patient_code = db.Column(db.String(50), nullable=False)
    format = db.Column(db.String(10), nullable=False) # 'PDF', 'CSV'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemMetric(db.Model):
    """System Latency & Sub-Second SLA Tracking"""
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(100), nullable=False)
    latency_ms = db.Column(db.Float, nullable=False)
    status_code = db.Column(db.Integer, nullable=False, default=200)
    meets_sla = db.Column(db.Integer, nullable=False, default=1) # 1 if latency < 1000ms
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
