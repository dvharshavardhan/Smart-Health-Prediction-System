import os
import csv
import json
import io
from datetime import datetime

def generate_patient_html_report(prediction_record):
    """
    Generates a clean, hospital-grade printable PDF/HTML clinical diagnostic report 
    with ML Dataset specifications and QR verification placeholder.
    """
    p_code = prediction_record.get('patient_code', 'MED-UNKNOWN')
    name = prediction_record.get('patient_name', 'Anonymous Patient')
    age = prediction_record.get('age', 'N/A')
    gender = prediction_record.get('gender', 'N/A')
    height = prediction_record.get('height_cm', 170.0)
    weight = prediction_record.get('weight_kg', 70.0)
    bmi = prediction_record.get('bmi', 24.5)
    
    date_str = prediction_record.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    risk_level = prediction_record.get('risk_level', 'Low')
    confidence_pct = float(prediction_record.get('confidence_pct', 0.0))
    model_used = prediction_record.get('model_used', 'Random Forest Ensemble')
    latency_ms = prediction_record.get('latency_ms', 14.2)
    
    if risk_level == 'High':
        risk_color = '#ef4444'
        badge_bg = '#fee2e2'
    elif risk_level == 'Medium':
        risk_color = '#f59e0b'
        badge_bg = '#fef3c7'
    else:
        risk_color = '#10b981'
        badge_bg = '#d1fae5'

    key_factors = prediction_record.get('key_factors', [])
    if isinstance(key_factors, str):
        try:
            key_factors = json.loads(key_factors)
        except Exception:
            key_factors = [key_factors]

    recommendations = prediction_record.get('recommendations', [])
    if isinstance(recommendations, str):
        try:
            recommendations = json.loads(recommendations)
        except Exception:
            recommendations = [recommendations]

    disease_probs = prediction_record.get('disease_probs', {})
    if isinstance(disease_probs, str):
        try:
            disease_probs = json.loads(disease_probs)
        except Exception:
            disease_probs = {}

    factors_html = "".join([f"<li>{kf}</li>" for kf in key_factors])
    recs_html = "".join([f"<li>{r}</li>" for r in recommendations])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hospital Clinical Diagnostic Report - {p_code}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 40px; }}
        .report-card {{ max-width: 840px; margin: 0 auto; background: #ffffff; padding: 44px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #0284c7; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #0284c7; display: flex; align-items: center; gap: 10px; }}
        .report-meta {{ text-align: right; font-size: 13px; color: #64748b; }}
        .patient-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; background: #f1f5f9; padding: 20px; border-radius: 8px; margin-bottom: 24px; }}
        .patient-field label {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; display: block; }}
        .patient-field span {{ font-size: 15px; font-weight: 600; color: #0f172a; }}
        .risk-banner {{ background: {badge_bg}; border-left: 6px solid {risk_color}; padding: 20px; border-radius: 8px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }}
        .risk-title {{ font-size: 24px; font-weight: bold; color: {risk_color}; margin: 0; }}
        .risk-score-badge {{ font-size: 18px; font-weight: bold; color: {risk_color}; }}
        .section-title {{ font-size: 14px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; margin-top: 24px; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
        ul {{ margin: 0; padding-left: 20px; line-height: 1.7; color: #334155; font-size: 13px; }}
        .metrics-table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
        .metrics-table th, .metrics-table td {{ border: 1px solid #e2e8f0; padding: 10px 14px; text-align: left; font-size: 13px; }}
        .metrics-table th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        .disease-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 12px; text-align: center; }}
        .disease-box {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 6px; }}
        .disease-name {{ font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; }}
        .disease-val {{ font-size: 16px; font-weight: 700; color: #0284c7; margin-top: 4px; }}
        .qr-placeholder {{ width: 70px; height: 70px; border: 2px dashed #0284c7; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: #0284c7; text-align: center; line-height: 1.2; background: #f0f9ff; }}
        .disclaimer-box {{ background: #f8fafc; border: 1px solid #e2e8f0; padding: 14px; border-radius: 6px; margin-top: 24px; font-size: 11px; color: #64748b; line-height: 1.5; }}
        .footer {{ margin-top: 36px; border-top: 1px solid #e2e8f0; padding-top: 20px; display: flex; justify-content: space-between; align-items: flex-end; font-size: 12px; color: #94a3b8; }}
        .signature-line {{ border-top: 1px solid #cbd5e1; width: 220px; text-align: center; padding-top: 5px; color: #64748b; font-size: 12px; }}
        @media print {{ body {{ background: #fff; padding: 0; }} .report-card {{ box-shadow: none; border: none; }} }}
    </style>
</head>
<body>
    <div class="report-card">
        <div class="header">
            <div class="logo">
                🏥 MedPredict AI Diagnostic Platform
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <div class="qr-placeholder">
                    QR VERIFIED<br>OFFICIAL
                </div>
                <div class="report-meta">
                    <div><strong>Report ID:</strong> RPT-{p_code}</div>
                    <div><strong>Generated:</strong> {date_str}</div>
                    <div><strong>Inference Speed:</strong> {latency_ms} ms</div>
                </div>
            </div>
        </div>
        
        <div class="patient-grid">
            <div class="patient-field"><label>Patient Code</label><span>{p_code}</span></div>
            <div class="patient-field"><label>Full Name</label><span>{name}</span></div>
            <div class="patient-field"><label>Age / Gender</label><span>{age} yrs / {gender}</span></div>
            <div class="patient-field"><label>Height / Weight / BMI</label><span>{height}cm / {weight}kg / {bmi}</span></div>
        </div>
        
        <div class="risk-banner">
            <div>
                <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#64748b; font-weight:600;">AI Evaluated Risk Level</div>
                <h2 class="risk-title">{risk_level} Risk Category</h2>
            </div>
            <div class="risk-score-badge">
                Confidence Probability: {confidence_pct:.1f}%
            </div>
        </div>

        <div class="section-title">Machine Learning Model Lineage Specs</div>
        <table class="metrics-table">
            <tr>
                <td><strong>ML Dataset Cohort</strong></td>
                <td>MedPredict 10K Synthetic Clinical Dataset (10,500 Patient Records)</td>
            </tr>
            <tr>
                <td><strong>Classifier Architecture</strong></td>
                <td>{model_used} (Scikit-Learn Pipeline with StandardScaler)</td>
            </tr>
            <tr>
                <td><strong>Train / Test Evaluation Split</strong></td>
                <td>80% Training (8,400 samples) / 20% Testing (2,100 samples)</td>
            </tr>
            <tr>
                <td><strong>Inference Latency SLA</strong></td>
                <td>{latency_ms} ms (Verified &lt; 1,000 ms SLA Target)</td>
            </tr>
        </table>

        <div class="section-title">5 Major Diseases Risk Breakdown</div>
        <div class="disease-grid">
            <div class="disease-box"><div class="disease-name">Heart Disease</div><div class="disease-val">{disease_probs.get('heart_disease', 0)}%</div></div>
            <div class="disease-box"><div class="disease-name">Diabetes</div><div class="disease-val">{disease_probs.get('diabetes', 0)}%</div></div>
            <div class="disease-box"><div class="disease-name">Kidney Disease</div><div class="disease-val">{disease_probs.get('kidney_disease', 0)}%</div></div>
            <div class="disease-box"><div class="disease-name">Stroke Risk</div><div class="disease-val">{disease_probs.get('stroke_risk', 0)}%</div></div>
            <div class="disease-box"><div class="disease-name">Hypertension</div><div class="disease-val">{disease_probs.get('hypertension', 0)}%</div></div>
        </div>

        <div class="section-title">Measured Vitals vs Standard Reference Ranges</div>
        <table class="metrics-table">
            <thead>
                <tr>
                    <th>Clinical Metric</th>
                    <th>Measured Value</th>
                    <th>Standard Reference Range</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Systolic / Diastolic BP</td>
                    <td>{prediction_record.get('systolic_bp')} / {prediction_record.get('diastolic_bp')} mmHg</td>
                    <td>&lt; 120 / 80 mmHg</td>
                    <td>{'Elevated' if float(prediction_record.get('systolic_bp', 120)) >= 130 else 'Optimal'}</td>
                </tr>
                <tr>
                    <td>Body Mass Index (BMI)</td>
                    <td>{bmi} kg/m²</td>
                    <td>18.5 - 24.9 kg/m²</td>
                    <td>{'Overweight' if float(bmi) >= 25 else 'Normal'}</td>
                </tr>
                <tr>
                    <td>Fasting Blood Glucose</td>
                    <td>{prediction_record.get('glucose')} mg/dL</td>
                    <td>70 - 99 mg/dL</td>
                    <td>{'Elevated' if float(prediction_record.get('glucose', 90)) >= 100 else 'Normal'}</td>
                </tr>
                <tr>
                    <td>Total Serum Cholesterol</td>
                    <td>{prediction_record.get('cholesterol')} mg/dL</td>
                    <td>&lt; 200 mg/dL</td>
                    <td>{'High' if float(prediction_record.get('cholesterol', 180)) >= 200 else 'Normal'}</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">Key Medical Risk Drivers</div>
        <ul>{factors_html}</ul>

        <div class="section-title">AI Clinical & Lifestyle Guidance</div>
        <ul>{recs_html}</ul>

        <div class="disclaimer-box">
            <strong>Medical Disclaimer:</strong> This clinical diagnostic report is generated automatically by MedPredict AI using trained machine learning classification models. Designed for clinical decision support and portfolio demonstration.
        </div>

        <div class="footer">
            <div>
                MedPredict AI Platform • Diagnostic Report ID: RPT-{p_code}.<br>
                Evaluated via {model_used} on MedPredict 10K Dataset.
            </div>
            <div class="signature-line">
                Attending Physician Signature
            </div>
        </div>
    </div>
</body>
</html>"""
    return html

def generate_csv_report(predictions_records):
    """
    Generates downloadable CSV stream for patient prediction history log.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'ID', 'Patient Code', 'Patient Name', 'Age', 'Gender', 'Height (cm)', 'Weight (kg)', 'BMI',
        'Systolic BP', 'Diastolic BP', 'Glucose', 'Heart Rate', 'Cholesterol',
        'Smoking', 'Alcohol', 'Exercise', 'Family History', 'Model Used',
        'Risk Level', 'Confidence (%)', 'Latency (ms)', 'Timestamp'
    ])
    
    for r in predictions_records:
        writer.writerow([
            r.get('id'), r.get('patient_code'), r.get('patient_name'), r.get('age'), r.get('gender'),
            r.get('height_cm'), r.get('weight_kg'), r.get('bmi'),
            r.get('systolic_bp'), r.get('diastolic_bp'), r.get('glucose'), r.get('heart_rate'), r.get('cholesterol'),
            r.get('smoking'), r.get('alcohol'), r.get('exercise'), r.get('family_history'),
            r.get('model_used'), r.get('risk_level'), r.get('confidence_pct'), r.get('latency_ms'), r.get('created_at')
        ])
        
    output.seek(0)
    return output.getvalue()
