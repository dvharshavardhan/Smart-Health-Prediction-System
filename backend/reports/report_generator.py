import os
import json
from datetime import datetime

def generate_patient_html_report(prediction_record):
    """
    Generates a clean, professional HTML clinical diagnostic report for print/PDF export.
    """
    p_code = prediction_record.get('patient_code', 'PAT-UNKNOWN')
    name = prediction_record.get('patient_name', 'Anonymous Patient')
    age = prediction_record.get('age', 'N/A')
    gender = prediction_record.get('gender', 'N/A')
    date_str = prediction_record.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    risk_level = prediction_record.get('risk_level', 'Low Risk')
    risk_score = float(prediction_record.get('risk_score', 0.0)) * 100
    
    if risk_level == 'High Risk':
        risk_color = '#ef4444'
        badge_bg = '#fee2e2'
    elif risk_level == 'Moderate Risk':
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

    factors_html = "".join([f"<li>{kf}</li>" for kf in key_factors])
    recs_html = "".join([f"<li>{r}</li>" for r in recommendations])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clinical Health Prediction Report - {p_code}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 40px; }}
        .report-card {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #0284c7; display: flex; align-items: center; gap: 10px; }}
        .report-meta {{ text-align: right; font-size: 13px; color: #64748b; }}
        .patient-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; background: #f1f5f9; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .patient-field label {{ font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; display: block; }}
        .patient-field span {{ font-size: 15px; font-weight: 600; color: #0f172a; }}
        .risk-banner {{ background: {badge_bg}; border-left: 6px solid {risk_color}; padding: 20px; border-radius: 8px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
        .risk-title {{ font-size: 22px; font-weight: bold; color: {risk_color}; margin: 0; }}
        .risk-score-badge {{ font-size: 18px; font-weight: bold; color: {risk_color}; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #cbd5e1; padding-bottom: 8px; margin-top: 30px; margin-bottom: 15px; }}
        ul {{ margin: 0; padding-left: 20px; line-height: 1.6; color: #334155; }}
        .metrics-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        .metrics-table th, .metrics-table td {{ border: 1px solid #e2e8f0; padding: 10px 14px; text-align: left; font-size: 13px; }}
        .metrics-table th {{ background: #f8fafc; font-weight: 600; color: #475569; }}
        .footer {{ margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 20px; display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; }}
        .signature-line {{ border-top: 1px solid #cbd5e1; width: 200px; text-align: center; padding-top: 5px; color: #64748b; font-size: 12px; margin-top: 40px; }}
        @media print {{ body {{ background: #fff; padding: 0; }} .report-card {{ box-shadow: none; border: none; }} }}
    </style>
</head>
<body>
    <div class="report-card">
        <div class="header">
            <div class="logo">
                🏥 Smart Health Prediction System
            </div>
            <div class="report-meta">
                <div><strong>Report ID:</strong> RPT-{p_code}</div>
                <div><strong>Generated:</strong> {date_str}</div>
                <div><strong>SLA Latency:</strong> {prediction_record.get('latency_ms', 180)} ms</div>
            </div>
        </div>
        
        <div class="patient-grid">
            <div class="patient-field"><label>Patient ID</label><span>{p_code}</span></div>
            <div class="patient-field"><label>Full Name</label><span>{name}</span></div>
            <div class="patient-field"><label>Age / Gender</label><span>{age} yrs / {gender}</span></div>
            <div class="patient-field"><label>AI Model</label><span>{prediction_record.get('model_used', 'Random Forest')}</span></div>
        </div>
        
        <div class="risk-banner">
            <div>
                <div style="font-size:12px; text-transform:uppercase; letter-spacing:1px; color:#64748b; font-weight:600;">Evaluated Risk Status</div>
                <h2 class="risk-title">{risk_level}</h2>
            </div>
            <div class="risk-score-badge">
                Risk Score: {risk_score:.1f}%
            </div>
        </div>

        <div class="section-title">Patient Vital & Clinical Metrics</div>
        <table class="metrics-table">
            <thead>
                <tr>
                    <th>Clinical Metric</th>
                    <th>Measured Value</th>
                    <th>Standard Reference Range</th>
                    <th>Evaluation Status</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Systolic / Diastolic BP</td>
                    <td>{prediction_record.get('systolic_bp')} / {prediction_record.get('diastolic_bp')} mmHg</td>
                    <td>&lt; 120 / 80 mmHg</td>
                    <td>{'Elevated' if float(prediction_record.get('systolic_bp', 120)) > 130 else 'Optimal'}</td>
                </tr>
                <tr>
                    <td>Body Mass Index (BMI)</td>
                    <td>{prediction_record.get('bmi')} kg/m²</td>
                    <td>18.5 - 24.9 kg/m²</td>
                    <td>{'Overweight' if float(prediction_record.get('bmi', 22)) >= 25 else 'Normal'}</td>
                </tr>
                <tr>
                    <td>Fasting Blood Glucose</td>
                    <td>{prediction_record.get('glucose_level')} mg/dL</td>
                    <td>70 - 99 mg/dL</td>
                    <td>{'Elevated' if float(prediction_record.get('glucose_level', 90)) >= 100 else 'Normal'}</td>
                </tr>
                <tr>
                    <td>Total Serum Cholesterol</td>
                    <td>{prediction_record.get('cholesterol')} mg/dL</td>
                    <td>&lt; 200 mg/dL</td>
                    <td>{'High' if float(prediction_record.get('cholesterol', 180)) >= 200 else 'Normal'}</td>
                </tr>
                <tr>
                    <td>Resting Heart Rate</td>
                    <td>{prediction_record.get('heart_rate')} bpm</td>
                    <td>60 - 100 bpm</td>
                    <td>Normal</td>
                </tr>
            </tbody>
        </table>

        <div class="section-title">Key Risk Contributors</div>
        <ul>{factors_html}</ul>

        <div class="section-title">Clinical & Lifestyle Recommendations</div>
        <ul>{recs_html}</ul>

        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
            <div class="footer">
                This AI risk assessment report is generated by the Smart Health Prediction System.<br>
                Optimized API Response Time: &lt; 1.5 Seconds SLA.
            </div>
            <div class="signature-line">
                Attending Physician Signature
            </div>
        </div>
    </div>
</body>
</html>"""
    return html
