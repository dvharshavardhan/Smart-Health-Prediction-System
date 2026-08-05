import os
import numpy as np
import pandas as pd

def generate_medical_dataset(num_records=10500, seed=42, output_path=None):
    """
    Generates a realistic 10,500+ patient medical dataset with clinical correlations.
    Covers Heart Disease, Diabetes, Kidney Disease, Stroke Risk, and Hypertension.
    """
    np.random.seed(seed)
    
    # 1. Demographics
    age = np.random.randint(18, 86, size=num_records)
    gender_num = np.random.choice([0, 1], size=num_records, p=[0.51, 0.49]) # 0: Female, 1: Male
    gender_str = np.where(gender_num == 1, 'Male', 'Female')
    
    height_cm = np.clip(np.random.normal(168, 10, size=num_records), 145, 205)
    weight_kg = np.clip(np.random.normal(72, 14, size=num_records), 42, 140)
    height_m = height_cm / 100.0
    bmi = np.round(weight_kg / (height_m ** 2), 1)
    
    # 2. Vitals correlated with age & BMI
    systolic_bp = np.clip(100 + (age * 0.48) + (bmi * 0.65) + np.random.normal(0, 8, size=num_records), 90, 195)
    diastolic_bp = np.clip(60 + (age * 0.28) + (bmi * 0.38) + np.random.normal(0, 5, size=num_records), 55, 115)
    glucose = np.clip(75 + (bmi * 2.0) + (age * 0.35) + np.random.normal(0, 14, size=num_records), 65, 290)
    cholesterol = np.clip(140 + (age * 0.95) + (bmi * 1.2) + np.random.normal(0, 18, size=num_records), 110, 340)
    
    # 3. Lifestyle & History
    smoking = np.random.choice([0, 1, 2], size=num_records, p=[0.55, 0.25, 0.20]) # 0: Never, 1: Former, 2: Current
    alcohol = np.random.choice([0, 1, 2], size=num_records, p=[0.50, 0.35, 0.15]) # 0: None, 1: Moderate, 2: Heavy
    exercise = np.random.choice([0, 1, 2], size=num_records, p=[0.30, 0.45, 0.25]) # 0: Low, 1: Moderate, 2: High
    heart_rate = np.clip(60 + (bmi * 0.4) - (exercise * 4) + np.random.normal(0, 6, size=num_records), 50, 115)
    family_history = np.random.choice([0, 1], size=num_records, p=[0.65, 0.35])
    
    # 4. Clinical Disease Flag Rules
    heart_disease = np.where((systolic_bp > 135) | (cholesterol > 220) | (smoking == 2), 1, 0)
    diabetes = np.where((glucose > 125) | (bmi > 30.0), 1, 0)
    kidney_disease = np.where((systolic_bp > 140) & (glucose > 130), 1, 0)
    stroke_risk = np.where((systolic_bp > 145) & (age > 55), 1, 0)
    hypertension = np.where((systolic_bp >= 130) | (diastolic_bp >= 80), 1, 0)
    
    # 5. Overall Risk Score Calculation
    score_raw = (
        (age * 0.040) +
        ((systolic_bp - 120) * 0.045) +
        ((diastolic_bp - 80) * 0.028) +
        ((bmi - 24.5) * 0.065) +
        ((glucose - 100) * 0.030) +
        ((cholesterol - 190) * 0.018) +
        (smoking * 0.60) +
        (alcohol * 0.35) -
        (exercise * 0.45) +
        (family_history * 0.75) +
        np.random.normal(0, 0.50, size=num_records)
    )
    
    q1, q2 = np.percentile(score_raw, [36, 74])
    health_risk_level = np.zeros(num_records, dtype=int)
    health_risk_level[score_raw >= q1] = 1 # Medium Risk
    health_risk_level[score_raw >= q2] = 2 # High Risk
    
    df = pd.DataFrame({
        'age': np.round(age).astype(int),
        'gender': gender_str,
        'gender_code': gender_num,
        'height_cm': np.round(height_cm, 1),
        'weight_kg': np.round(weight_kg, 1),
        'bmi': np.round(bmi, 1),
        'systolic_bp': np.round(systolic_bp, 1),
        'diastolic_bp': np.round(diastolic_bp, 1),
        'glucose': np.round(glucose, 1),
        'cholesterol': np.round(cholesterol, 1),
        'heart_rate': np.round(heart_rate).astype(int),
        'smoking': smoking,
        'alcohol': alcohol,
        'exercise': exercise,
        'family_history': family_history,
        'heart_disease': heart_disease,
        'diabetes': diabetes,
        'kidney_disease': kidney_disease,
        'stroke_risk': stroke_risk,
        'hypertension': hypertension,
        'health_risk_level': health_risk_level
    })
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Generated dataset with {len(df)} records at '{output_path}'.")
        
    return df

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, 'datasets', 'medpredict_10k.csv')
    generate_medical_dataset(10500, output_path=csv_file)
