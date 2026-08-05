import random
import json
from datetime import datetime, timedelta
from database import db
from database.models import Patient, Prediction, ModelMetric, SystemMetric, ReportLog

def init_db(app):
    """Initializes SQLAlchemy Database and seeds initial records if empty."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_database_if_empty()

def seed_database_if_empty():
    """Seeds database with 520 realistic healthcare records, report logs & SLA metrics."""
    if Prediction.query.count() >= 500:
        return

    print("Seeding database with 520 enterprise patient records & SLA metrics...")
    
    first_names = ["Alexander", "Sophia", "Ethan", "Olivia", "Liam", "Emma", "Noah", "Ava", "William", "Isabella", "James", "Mia", "Benjamin", "Charlotte", "Lucas"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    models = ["Random Forest", "Logistic Regression", "Decision Tree"]
    
    base_time = datetime.utcnow() - timedelta(days=60)
    
    for i in range(1, 521):
        p_code = f"MED-{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(20, 84)
        gender = random.choice(["Male", "Female"])
        height_cm = round(random.uniform(155.0, 190.0), 1)
        weight_kg = round(random.uniform(50.0, 110.0), 1)
        height_m = height_cm / 100.0
        bmi = round(weight_kg / (height_m * height_m), 1)
        
        systolic = round(random.uniform(105, 175), 1)
        diastolic = round(random.uniform(65, 108), 1)
        glucose = round(random.uniform(78, 230), 1)
        cholesterol = round(random.uniform(145, 310), 1)
        hr = random.randint(58, 104)
        
        smoking = random.choice([0, 1, 2])
        alcohol = random.choice([0, 1, 2])
        exercise = random.choice([0, 1, 2])
        family_history = random.choice([0, 1])
        
        # Risk score calculation
        score_raw = (age * 0.015) + (systolic * 0.01) + (glucose * 0.008) + (bmi * 0.02) + (smoking * 0.15) - (exercise * 0.1)
        risk_score = min(max((score_raw - 1.1) / 3.0, 0.05), 0.98)
        
        if risk_score < 0.35:
            risk_level = "Low"
        elif risk_score < 0.70:
            risk_level = "Medium"
        else:
            risk_level = "High"
            
        confidence_pct = round(risk_score * 100, 2)
        
        # 5 Disease probabilities
        disease_probs = {
            'heart_disease': round(min(max((systolic/180.0)*50 + (cholesterol/300.0)*40 + (smoking*10), 8.0), 98.0), 1),
            'diabetes': round(min(max((glucose/240.0)*60 + (bmi/40.0)*30, 6.0), 96.0), 1),
            'kidney_disease': round(min(max((systolic/190.0)*45 + (glucose/250.0)*45, 4.0), 92.0), 1),
            'stroke_risk': round(min(max((systolic/190.0)*60 + (age/90.0)*30, 5.0), 95.0), 1),
            'hypertension': round(min(max((systolic/180.0)*70 + (diastolic/110.0)*30, 10.0), 99.0), 1)
        }
        
        key_factors = []
        if systolic >= 130:
            key_factors.append(f"Elevated Blood Pressure ({int(systolic)}/{int(diastolic)} mmHg)")
        if bmi >= 25.0:
            key_factors.append(f"Elevated BMI ({bmi} kg/m²)")
        if glucose >= 110:
            key_factors.append(f"Elevated Fasting Glucose ({int(glucose)} mg/dL)")
        if cholesterol >= 200:
            key_factors.append(f"High Serum Cholesterol ({int(cholesterol)} mg/dL)")
        if smoking > 0:
            key_factors.append("Tobacco Use / Smoking History")
        if not key_factors:
            key_factors.append("Vitals within normal clinical reference ranges")
            
        recommendations = []
        if risk_level == "High":
            recommendations.append("Schedule an immediate comprehensive cardiovascular consultation.")
            recommendations.append("Adopt a low-sodium, heart-healthy DASH dietary protocol.")
            recommendations.append("Monitor blood pressure and fasting blood glucose daily.")
        elif risk_level == "Medium":
            recommendations.append("Increase moderate aerobic physical activity to 150+ mins/week.")
            recommendations.append("Reduce intake of refined sugars and saturated fats.")
            recommendations.append("Schedule a routine annual preventive screening.")
        else:
            recommendations.append("Maintain current healthy dietary and physical activity routine.")
            recommendations.append("Continue regular wellness checkups.")

        latency = round(random.uniform(120.0, 380.0), 2) # Sub-1-second SLA (<1000ms)
        created_at = base_time + timedelta(hours=i * 2.7)
        
        patient = Patient(
            patient_code=p_code,
            name=name,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg,
            bmi=bmi,
            created_at=created_at
        )
        db.session.add(patient)
        db.session.flush() # assign patient.id
        
        pred = Prediction(
            patient_id=patient.id,
            patient_code=p_code,
            patient_name=name,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg,
            bmi=bmi,
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            glucose=glucose,
            heart_rate=hr,
            cholesterol=cholesterol,
            smoking=smoking,
            alcohol=alcohol,
            exercise=exercise,
            family_history=family_history,
            model_used=random.choice(models),
            risk_level=risk_level,
            confidence_pct=confidence_pct,
            disease_probs_json=json.dumps(disease_probs),
            recommendations_json=json.dumps(recommendations),
            key_factors_json=json.dumps(key_factors),
            latency_ms=latency,
            created_at=created_at
        )
        db.session.add(pred)
        
        metric = SystemMetric(
            endpoint='/api/predict',
            latency_ms=latency,
            status_code=200,
            meets_sla=1,
            timestamp=created_at
        )
        db.session.add(metric)

        # Seed Report Log for subset of patients
        if i % 4 == 0:
            report = ReportLog(
                report_code=f"RPT-{p_code}-{i}",
                patient_code=p_code,
                format="PDF",
                created_at=created_at
            )
            db.session.add(report)

    # Initial Model Metrics
    initial_metrics = [
        ModelMetric(
            model_name="Random Forest",
            accuracy=0.8850,
            precision=0.8790,
            recall=0.8820,
            f1_score=0.8805,
            confusion_matrix_json=json.dumps([[142, 12, 4], [10, 130, 8], [3, 9, 132]])
        ),
        ModelMetric(
            model_name="Logistic Regression",
            accuracy=0.8420,
            precision=0.8350,
            recall=0.8410,
            f1_score=0.8380,
            confusion_matrix_json=json.dumps([[135, 18, 5], [14, 122, 12], [6, 12, 126]])
        ),
        ModelMetric(
            model_name="Decision Tree",
            accuracy=0.7950,
            precision=0.7910,
            recall=0.7940,
            f1_score=0.7925,
            confusion_matrix_json=json.dumps([[128, 22, 8], [18, 115, 15], [9, 16, 119]])
        )
    ]
    db.session.add_all(initial_metrics)
    db.session.commit()
    print("Database seeding completed successfully with 130+ initial ReportLog entries.")
