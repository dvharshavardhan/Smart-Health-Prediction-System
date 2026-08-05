import os
import numpy as np
import pandas as pd

def generate_healthcare_dataset(num_records=10500, seed=42, output_path=None):
    """
    Generates a realistic synthetic healthcare dataset with 10,000+ patient records.
    Establishes clinical feature correlations to achieve ~85% prediction accuracy.
    """
    np.random.seed(seed)
    
    # 1. Demographic parameters
    age = np.random.randint(18, 86, size=num_records)
    gender_num = np.random.choice([0, 1], size=num_records, p=[0.51, 0.49]) # 0: Female, 1: Male
    gender_str = np.where(gender_num == 1, 'Male', 'Female')
    
    # 2. Vital metrics with age/gender correlations
    bmi_base = np.random.normal(25.5, 5.0, size=num_records)
    bmi = np.clip(bmi_base + (age * 0.06), 16.0, 48.0)
    
    # Systolic & Diastolic BP correlated with age and BMI
    systolic_bp = np.clip(100 + (age * 0.50) + (bmi * 0.70) + np.random.normal(0, 8, size=num_records), 90, 195)
    diastolic_bp = np.clip(60 + (age * 0.28) + (bmi * 0.40) + np.random.normal(0, 5, size=num_records), 55, 115)
    
    # Glucose level (mg/dL) correlated with BMI & Age
    glucose_level = np.clip(75 + (bmi * 2.1) + (age * 0.35) + np.random.normal(0, 14, size=num_records), 65, 290)
    
    # Cholesterol level (mg/dL)
    cholesterol = np.clip(140 + (age * 1.0) + (bmi * 1.3) + np.random.normal(0, 18, size=num_records), 110, 340)
    
    # Lifestyle factors
    smoking_status = np.random.choice([0, 1, 2], size=num_records, p=[0.55, 0.25, 0.20]) # 0: Never, 1: Former, 2: Current
    physical_activity = np.random.choice([0, 1, 2], size=num_records, p=[0.30, 0.45, 0.25]) # 0: Low, 1: Moderate, 2: High
    heart_rate = np.clip(60 + (bmi * 0.4) - (physical_activity * 4) + np.random.normal(0, 6, size=num_records), 50, 115)
    family_history = np.random.choice([0, 1], size=num_records, p=[0.65, 0.35])
    
    # 3. Clinical Risk Score Computation
    risk_score = (
        (age * 0.040) +
        ((systolic_bp - 120) * 0.045) +
        ((diastolic_bp - 80) * 0.028) +
        ((bmi - 24.5) * 0.065) +
        ((glucose_level - 100) * 0.030) +
        ((cholesterol - 190) * 0.018) +
        (smoking_status * 0.65) -
        (physical_activity * 0.45) +
        (family_history * 0.80) +
        np.random.normal(0, 0.55, size=num_records)
    )
    
    q1, q2 = np.percentile(risk_score, [36, 74])
    health_risk_level = np.zeros(num_records, dtype=int)
    health_risk_level[risk_score >= q1] = 1
    health_risk_level[risk_score >= q2] = 2
    
    cardiovascular_risk = np.where((systolic_bp > 135) | (cholesterol > 220) | (risk_score > 2.0), 1, 0)
    diabetes_risk = np.where((glucose_level > 125) | (bmi > 30.0) | (risk_score > 1.8), 1, 0)
    kidney_risk = np.where((systolic_bp > 140) & (glucose_level > 130), 1, 0)
    
    df = pd.DataFrame({
        'age': np.round(age).astype(int),
        'gender': gender_str,
        'gender_code': gender_num,
        'systolic_bp': np.round(systolic_bp, 1),
        'diastolic_bp': np.round(diastolic_bp, 1),
        'bmi': np.round(bmi, 1),
        'glucose_level': np.round(glucose_level, 1),
        'cholesterol': np.round(cholesterol, 1),
        'smoking_status': smoking_status,
        'physical_activity': physical_activity,
        'heart_rate': np.round(heart_rate).astype(int),
        'family_history': family_history,
        'cardiovascular_risk': cardiovascular_risk,
        'diabetes_risk': diabetes_risk,
        'kidney_risk': kidney_risk,
        'health_risk_level': health_risk_level
    })
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} healthcare records at '{output_path}'.")
        
    return df

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_file = os.path.join(base_dir, 'data', 'healthcare_records_10k.csv')
    generate_healthcare_dataset(10500, output_path=out_file)
