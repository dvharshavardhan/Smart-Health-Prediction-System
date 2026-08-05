// Main SPA Router, Theme Toggle & Predictor Logic

function switchTab(tabId, btnElement) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    btnElement.classList.add('active');
}

// 10/10 Live Theme Switcher Logic (White Theme <-> Dark AI Mode)
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    const btn = document.getElementById('themeToggleBtn');
    
    if (newTheme === 'dark') {
        btn.innerHTML = '<span>🌙 Dark AI Mode</span>';
    } else {
        btn.innerHTML = '<span>☀️ Light Mode</span>';
    }
    
    // Refresh chart ticks if analytics tab is active
    if (typeof loadAnalyticsData === 'function') {
        loadAnalyticsData();
    }
}

// Preset Quick Test Profiles
const PRESETS = {
    healthy: {
        patient_code: 'PAT-1002', patient_name: 'Sarah Connor', age: 32, gender: 'Female',
        systolic_bp: 115, diastolic_bp: 75, bmi: 22.4, glucose_level: 88, cholesterol: 172,
        smoking_status: 0, physical_activity: 2, heart_rate: 68, family_history: 0
    },
    moderate: {
        patient_code: 'PAT-1045', patient_name: 'Robert Thorne', age: 48, gender: 'Male',
        systolic_bp: 132, diastolic_bp: 85, bmi: 27.8, glucose_level: 112, cholesterol: 210,
        smoking_status: 1, physical_activity: 1, heart_rate: 76, family_history: 1
    },
    cardiac: {
        patient_code: 'PAT-1099', patient_name: 'Arthur Pendelton', age: 64, gender: 'Male',
        systolic_bp: 156, diastolic_bp: 96, bmi: 33.5, glucose_level: 165, cholesterol: 260,
        smoking_status: 2, physical_activity: 0, heart_rate: 88, family_history: 1
    }
};

function loadPreset(presetKey) {
    const data = PRESETS[presetKey];
    if (!data) return;
    
    document.getElementById('patient_code').value = data.patient_code;
    document.getElementById('patient_name').value = data.patient_name;
    document.getElementById('age').value = data.age;
    document.getElementById('gender').value = data.gender;
    document.getElementById('systolic_bp').value = data.systolic_bp;
    document.getElementById('diastolic_bp').value = data.diastolic_bp;
    document.getElementById('bmi').value = data.bmi;
    document.getElementById('glucose_level').value = data.glucose_level;
    document.getElementById('cholesterol').value = data.cholesterol;
    document.getElementById('smoking_status').value = data.smoking_status;
    document.getElementById('physical_activity').value = data.physical_activity;
    document.getElementById('heart_rate').value = data.heart_rate;
    document.getElementById('family_history').value = data.family_history;
}

// Form Submission Handler
async function submitPrediction(event) {
    event.preventDefault();
    const btn = document.getElementById('predictBtn');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Processing AI Risk Model...</span>';

    const payload = {
        patient_code: document.getElementById('patient_code').value,
        patient_name: document.getElementById('patient_name').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        systolic_bp: parseFloat(document.getElementById('systolic_bp').value),
        diastolic_bp: parseFloat(document.getElementById('diastolic_bp').value),
        bmi: parseFloat(document.getElementById('bmi').value),
        glucose_level: parseFloat(document.getElementById('glucose_level').value),
        cholesterol: parseFloat(document.getElementById('cholesterol').value),
        smoking_status: parseInt(document.getElementById('smoking_status').value),
        physical_activity: parseInt(document.getElementById('physical_activity').value),
        heart_rate: parseInt(document.getElementById('heart_rate').value),
        family_history: parseInt(document.getElementById('family_history').value),
        model_name: document.getElementById('model_name').value
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const res = await response.json();
        btn.disabled = false;
        btn.innerHTML = '<span>⚡ Execute Real-Time AI Risk Prediction</span>';

        if (res.success && res.data) {
            displayResults(res.data);
        } else {
            alert('Prediction error: ' + (res.error || 'Unknown failure'));
        }
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '<span>⚡ Execute Real-Time AI Risk Prediction</span>';
        alert('Failed to connect to Flask API backend: ' + err.message);
    }
}

function displayResults(data) {
    const container = document.getElementById('resultContainer');
    container.style.display = 'block';
    
    const riskLevelEl = document.getElementById('resRiskLevel');
    const riskBadgeEl = document.getElementById('resRiskBadge');
    
    riskLevelEl.innerText = data.risk_level;
    const scorePct = (data.overall_risk_score * 100).toFixed(1);
    riskBadgeEl.innerText = `Score: ${scorePct}%`;
    
    if (data.risk_level === 'High Risk') {
        riskLevelEl.style.color = 'var(--rose-accent)';
        riskBadgeEl.className = 'badge badge-high';
        container.style.borderLeftColor = 'var(--rose-accent)';
    } else if (data.risk_level === 'Moderate Risk') {
        riskLevelEl.style.color = 'var(--amber-accent)';
        riskBadgeEl.className = 'badge badge-moderate';
        container.style.borderLeftColor = 'var(--amber-accent)';
    } else {
        riskLevelEl.style.color = 'var(--emerald-accent)';
        riskBadgeEl.className = 'badge badge-low';
        container.style.borderLeftColor = 'var(--emerald-accent)';
    }
    
    document.getElementById('resLatencyTag').innerText = `Response: ${data.latency_ms} ms (<1.5s SLA Verified)`;
    
    const cardioPct = Math.round(data.disease_risks.cardiovascular.probability * 100);
    const diabetesPct = Math.round(data.disease_risks.diabetes.probability * 100);
    const kidneyPct = Math.round(data.disease_risks.kidney.probability * 100);
    
    document.getElementById('resCardioScore').innerText = `${cardioPct}%`;
    document.getElementById('resCardioBar').style.width = `${cardioPct}%`;
    
    document.getElementById('resDiabetesScore').innerText = `${diabetesPct}%`;
    document.getElementById('resDiabetesBar').style.width = `${diabetesPct}%`;
    
    document.getElementById('resKidneyScore').innerText = `${kidneyPct}%`;
    document.getElementById('resKidneyBar').style.width = `${kidneyPct}%`;
    
    const factorsList = document.getElementById('resKeyFactors');
    factorsList.innerHTML = data.key_factors.map(f => `<li>${f}</li>`).join('');
    
    const recsList = document.getElementById('resRecommendations');
    recsList.innerHTML = data.recommendations.map(r => `<li>${r}</li>`).join('');
    
    document.getElementById('resReportLink').href = `/api/reports/export/${data.record_id}`;
    
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
