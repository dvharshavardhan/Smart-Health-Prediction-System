import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Enterprise Configuration Class for MedPredict AI Platform"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'medpredict-ai-enterprise-secret-key-2026')
    
    # SQLite Database URI using SQLAlchemy
    DB_DIR = os.path.join(BASE_DIR, 'database')
    os.makedirs(DB_DIR, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DB_DIR, 'medpredict.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML Engine & Directory Paths
    DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
    MODELS_DIR = os.path.join(BASE_DIR, 'trained_models')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # SLA & SLA Performance Standards (< 1.0 second execution target)
    SLA_LATENCY_MAX_MS = 1000.0
    TARGET_ACCURACY = 0.85
