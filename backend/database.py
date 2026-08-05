import os
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'health_system.db')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Patients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # 2. Prediction Records Table (Indexed for <1.5s query SLA)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            patient_code TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            systolic_bp REAL NOT NULL,
            diastolic_bp REAL NOT NULL,
            bmi REAL NOT NULL,
            glucose_level REAL NOT NULL,
            cholesterol REAL NOT NULL,
            smoking_status INTEGER NOT NULL,
            physical_activity INTEGER NOT NULL,
            heart_rate INTEGER NOT NULL,
            family_history INTEGER NOT NULL,
            model_used TEXT NOT NULL,
            risk_level TEXT NOT NULL,         -- 'Low Risk', 'Moderate Risk', 'High Risk'
            risk_score REAL NOT NULL,         -- Probability (0.0 to 1.0)
            cardio_risk INTEGER NOT NULL,
            diabetes_risk INTEGER NOT NULL,
            kidney_risk INTEGER NOT NULL,
            key_factors TEXT,                 -- JSON array string
            recommendations TEXT,             -- JSON array string
            latency_ms REAL NOT NULL,         -- Response latency metric
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        );
    ''')
    
    # Performance Indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_risk ON predictions (risk_level);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_date ON predictions (created_at DESC);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions_patient ON predictions (patient_code);')
    
    # 3. System Metrics Table (For monitoring API latency <1.5s SLA and +40% efficiency)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            status_code INTEGER NOT NULL,
            meets_sla INTEGER NOT NULL,        -- 1 if latency < 1500ms, 0 otherwise
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_metrics_time ON system_metrics (timestamp DESC);')

    # 4. Audit & Troubleshooting Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,            -- 'API', 'ML_MODEL', 'DATABASE', 'REPORT_GEN'
            log_level TEXT NOT NULL,           -- 'INFO', 'WARNING', 'ERROR'
            message TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.commit()
    conn.close()
    
    # Seed 500+ records if empty
    seed_database_if_empty()

def seed_database_if_empty():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM predictions;')
    row = cursor.fetchone()
    if row['count'] >= 500:
        conn.close()
        return

    print("Seeding SQLite database with 520 realistic patient prediction records...")
    
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley", "Avery", "Dakota", "Reese", "Casey", "Skyler", "Cameron", "Jesse"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    models = ["Random Forest", "Logistic Regression", "Decision Tree"]

    base_time = datetime.now() - timedelta(days=60)
    
    records = []
    audit_records = []
    metric_records = []
    
    for i in range(1, 521):
        p_code = f"PAT-{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(20, 82)
        gender = random.choice(["Male", "Female"])
        
        bmi = round(random.uniform(18.5, 38.0), 1)
        systolic = round(random.uniform(105, 175), 1)
        diastolic = round(random.uniform(68, 105), 1)
        glucose = round(random.uniform(78, 230), 1)
        cholesterol = round(random.uniform(150, 310), 1)
        smoking = random.choice([0, 1, 2])
        activity = random.choice([0, 1, 2])
        hr = random.randint(58, 102)
        family_hx = random.choice([0, 1])
        
        # Risk score simulation
        score_raw = (age*0.015) + (systolic*0.01) + (glucose*0.008) + (bmi*0.02) + (smoking*0.15) - (activity*0.1)
        risk_score = round(min(max((score_raw - 1.2) / 3.0, 0.05), 0.98), 4)
        
        if risk_score < 0.35:
            risk_level = "Low Risk"
        elif risk_score < 0.70:
            risk_level = "Moderate Risk"
        else:
            risk_level = "High Risk"
            
        cardio = 1 if (systolic > 135 or cholesterol > 230 or risk_score > 0.6) else 0
        diabetes = 1 if (glucose > 125 or bmi > 30.0 or risk_score > 0.5) else 0
        kidney = 1 if (systolic > 145 and glucose > 140) else 0
        
        latency = round(random.uniform(120.0, 480.0), 2) # Well within <1.5s SLA (<1500ms)
        created_at = (base_time + timedelta(hours=i * 2.7)).strftime('%Y-%m-%d %H:%M:%S')
        
        records.append((
            p_code, name, age, gender, systolic, diastolic, bmi, glucose, cholesterol,
            smoking, activity, hr, family_hx, random.choice(models), risk_level, risk_score,
            cardio, diabetes, kidney,
            '["Elevated BP", "Higher BMI"]', '["Adopt DASH diet", "Exercise 150m/week"]',
            latency, created_at
        ))
        
        metric_records.append(('/api/predict', latency, 200, 1, created_at))
        
        if i % 50 == 0:
            audit_records.append(('API', 'INFO', f'Processed patient batch prediction record {p_code}', f'Latency: {latency}ms', created_at))

    cursor.executemany('''
        INSERT INTO predictions (
            patient_code, patient_name, age, gender, systolic_bp, diastolic_bp, bmi,
            glucose_level, cholesterol, smoking_status, physical_activity, heart_rate,
            family_history, model_used, risk_level, risk_score, cardio_risk, diabetes_risk,
            kidney_risk, key_factors, recommendations, latency_ms, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', records)

    cursor.executemany('''
        INSERT INTO system_metrics (endpoint, latency_ms, status_code, meets_sla, timestamp)
        VALUES (?, ?, ?, ?, ?);
    ''', metric_records)

    cursor.executemany('''
        INSERT INTO audit_logs (category, log_level, message, details, timestamp)
        VALUES (?, ?, ?, ?, ?);
    ''', audit_records)

    conn.commit()
    conn.close()
    print("SQLite database successfully populated with 520 initial prediction records.")

if __name__ == '__main__':
    init_db()
