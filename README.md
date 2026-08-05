# 🏥 MedPredict AI – Intelligent Healthcare Analytics Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![Docker Ready](https://img.shields.io/badge/Docker-Multi--Stage-blue.svg)](Dockerfile)
[![CI Pipeline](https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen.svg)](.github/workflows/ci.yml)
[![Low Latency](https://img.shields.io/badge/Inference-Low--Latency-brightgreen.svg)](#performance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**MedPredict AI** is a portfolio-quality, full-stack multi-disease clinical risk prediction and population health analytics platform. Designed using enterprise software engineering practices, it features a **Python/Flask REST API**, **SQLAlchemy ORM database engine**, **Docker containerization**, **GitHub Actions CI/CD**, and a multi-model **Machine Learning suite** (Random Forest Ensemble, Logistic Regression, Decision Tree) optimized for real-time risk assessment across 5 critical medical conditions.

---

## 🎬 2–3 Minute Video Showcase & Interview Script

Follow this step-by-step workflow to record an impressive 2–3 minute video for LinkedIn, GitHub, or software engineering interviews:

| Time | Demonstration Step | Key Talking Points |
| :---: | :--- | :--- |
| **0:00 - 0:20** | **Executive Dashboard & Dataset Bar** | Open dashboard; point out the **10,500-record dataset summary bar** (`8,400 Train / 2,100 Test split`, 14 clinical features, and 5 supported conditions). |
| **0:20 - 0:45** | **ML Dataset & Benchmarks Tab** | Switch to *ML Benchmarks*; explain Scikit-Learn pipeline training, `StandardScaler` normalization, and Random Forest Ensemble selection (~88.5% accuracy). |
| **0:45 - 1:15** | **1-Click Demo Data & Input Vitals** | Click *Generate Random Demo Data*; show automatic BMI calculation and 14 clinical inputs (Blood Pressure, Fasting Glucose, Cholesterol). |
| **1:15 - 1:35** | **Multi-Stage AI Loading Sequence** | Click *Execute AI Risk Assessment*; highlight the 4-stage visual loading overlay (*Loading Model* → *Analyzing Vitals* → *Computing Risk*). |
| **1:35 - 2:00** | **Animated SVG Risk Meter & Results** | Review the **SVG Circular Risk Gauge Meter**, 5 Disease Breakdown bars, Key Risk Drivers, and AI Clinical Recommendations. |
| **2:00 - 2:20** | **Patient History & Table Sorting** | Open *History & Reports*; click table headers to demonstrate interactive column sorting (`Patient Code`, `Age`, `BMI`, `Risk Status`, `Latency`). |
| **2:20 - 2:40** | **Hospital Clinical PDF Report** | Click *Download Printable Clinical Report*; display official letterhead, `QR VERIFIED OFFICIAL` badge, vitals reference table, and ML model lineage specs. |
| **2:40 - 3:00** | **Telemetry Panel & Dark Mode** | Switch to *System Status* telemetry panel; toggle **1-Click Dark AI Mode** to highlight responsive dual theme support. |

---

## 🧠 Machine Learning Workflow & Lineage

The platform executes a transparent end-to-end machine learning pipeline:

```text
MedPredict 10K Dataset (10,500 Records)
           ↓
Data Cleaning & Feature Engineering (14 Clinical Vitals)
           ↓
Train / Test Evaluation Split (8,400 Train / 2,100 Test)
           ↓
Multi-Model Training (Random Forest, Logistic Regression, Decision Tree)
           ↓
Metric Benchmarking (Accuracy ~88.5%, Precision, Recall, F1 Score)
           ↓
Model Serialization (joblib: scaler.joblib & random_forest.joblib)
           ↓
Flask REST API Real-Time Inference (< 20ms Latency)
           ↓
SQLAlchemy ORM Storage & 6 Chart.js Analytics Dashboards
```

---

## 🌟 Key Architecture & UI Features

### 1. 🎨 Modern Glassmorphism SaaS Interface
* **Dual Theme Engine (1-Click Dark/Light Mode)**: Seamless CSS variable transitions between Clinical Light Mode and Dark AI Glassmorphism Theme.
* **Executive Hero Dashboard**: Includes real-time SLA compliance status, telemetry indicators, and live statistics.
* **Toast Notification System**: Non-intrusive floating toast stack replacing standard browser alerts.
* **Floating Action Button (FAB)**: Accessible 1-click shortcut for executing new clinical risk assessments.
* **5 Diseases Visual Breakdown**: Dynamic progress meters for **Heart Disease, Diabetes Type-2, Chronic Kidney Disease, Stroke Risk, and Hypertension**.

### 2. 🧠 Multi-Model Machine Learning Engine
* **Supervised Classifiers**: Evaluates and serializes **Random Forest Classifier (Ensemble Primary)**, **Logistic Regression**, and **Decision Tree** models.
* **Automated Model Evaluation**: Benchmarks Accuracy, Precision, Recall, F1 Score, and Confusion Matrices to evaluate classifier metrics.
* **Clinical Interpretability**: Highlights specific **Key Risk Factors** (e.g. *Elevated Systolic BP 144 mmHg*) and **AI Recommendations** (e.g. *Low-sodium DASH protocol*).

### 3. ⚡ Low-Latency Inference Pipeline
* **Telemetry Middleware**: Automatically tracks and records API response times per request to a dedicated `system_metrics` database table.
* **Production-Oriented Performance**: Optimized for fast REST API response times and verified against a 1-second SLA target.

### 4. 📊 Patient History Logs & Interactive Sorting
* **Indexed Patient History**: 520+ pre-seeded realistic clinical prediction records.
* **Interactive Column Sorting**: Header-click sorting (`sortTable(column)`) by Patient Code, Name, Age, BMI, Risk Status, or Latency.
* **Multi-Criteria Search & Filtering**: Filter patients in real time by patient code/name, risk category (**Low, Medium, High**), or disease classification.

### 5. 🏥 Clinical Diagnostic Reports & Exports
* **Printable PDF/HTML Letterhead**: Features a clinical header, official **QR Code Verification badge** (`QR VERIFIED OFFICIAL`), vitals reference matrix, AI disclaimers, and physician signature lines.
* **CSV Data Streams**: 1-click exporter for historical prediction datasets.

---

## 🐳 Docker & DevOps Deployment

### 1. Run with Docker Compose (Recommended)
Launch the containerized application stack in detached mode:

```bash
docker compose up -d
```

Access the platform at: 🌐 **[http://localhost:5000](http://localhost:5000)**

### 2. Build Docker Image Manually
```bash
# Build multi-stage image
docker build -t medpredict-ai:latest .

# Run container
docker run -d -p 5000:5000 --name medpredict_app medpredict-ai:latest
```

---

## 📁 System Architecture & Directory Structure

```text
MedPredictAI/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI Workflow Pipeline
├── app.py                     # Main Flask REST API Controller & Route Handlers
├── config.py                  # Environment Configuration & Directory Paths
├── Dockerfile                 # Multi-Stage Production Docker Build
├── docker-compose.yml         # Container Orchestration Specification
├── .env.example               # Environment Variables Template
├── .gitignore                 # Version Control Exclusions
├── requirements.txt            # Python Package Dependencies
├── README.md                  # Project Architecture & Documentation
├── datasets/
│   ├── generate_dataset.py    # 10,500 Patient Synthetic Dataset Generator
│   └── medpredict_10k.csv     # Serialized Clinical Training CSV
├── trained_models/
│   ├── scaler.joblib          # StandardScaler Pipeline
│   ├── random_forest.joblib   # Primary Ensemble Classifier
│   ├── logistic_regression.joblib
│   ├── decision_tree.joblib
│   └── metrics.json           # Model Benchmarking Metrics Output
├── database/
│   ├── __init__.py            # SQLAlchemy Instance Setup
│   ├── db.py                  # Database Init & 520-Record Automated Seeder
│   ├── models.py              # Patient, Prediction, ModelMetric, ReportLog, SystemMetric Schemas
│   └── medpredict.db          # SQLite Database File
├── ml/
│   ├── __init__.py
│   ├── trainer.py             # Model Training, Cross-Validation & Metric Evaluator
│   └── predictor.py           # Real-Time Multi-Disease Risk Predictor Engine
├── reports/
│   ├── __init__.py
│   └── generator.py           # Printable PDF/HTML Exporter & CSV Stream Exporter
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphism Design System CSS
│   └── js/
│       ├── main.js            # Core App Logic, Theme Handler & Input Validator
│       ├── toast.js           # Floating Toast Notification Engine
│       ├── charts.js          # 6-Chart Visual Dashboards
│       └── admin.js           # Patient History, Table Sorting & Telemetry Controller
├── templates/
│   └── index.html             # Enterprise Dashboard Single-Page HTML
└── tests/
    └── test_app.py            # Automated Unittest Suite (7/7 Passed)
```

---

## 📡 REST API Documentation

| Endpoint | Method | Description | Sample Response |
| :--- | :---: | :--- | :--- |
| `GET /` | `GET` | Renders main executive SaaS dashboard | `200 OK (HTML)` |
| `POST /api/predict` | `POST` | Multi-disease risk evaluation | `{"success": true, "data": {...}}` |
| `GET /api/patients` | `GET` | Paginated search, multi-filter & column-sorted logs | `{"total": 520, "records": [...]}` |
| `GET /api/system/status`| `GET` | Live telemetry (DB, ML, API speed, storage) | `{"status": {"database": "Connected"}}` |
| `GET /api/reports/export/<id>`| `GET` | Generates printable PDF/HTML clinical report | `200 OK (HTML/PDF)` |
| `GET /api/reports/export_csv` | `GET` | Downloads full prediction history CSV stream | `200 OK (text/csv)` |
| `GET /api/analytics` | `GET` | Aggregates risk breakdown, SLA %, & prevalence | `{"sla_compliance_percent": 100}` |
| `GET /api/models/metrics` | `GET` | Returns ML classifier benchmarks & confusion matrices | `{"metrics": {...}}` |
| `DELETE /api/prediction/<id>`| `DELETE`| Removes patient prediction record from database | `{"success": true}` |
| `GET /api/health` | `GET` | System health check & SLA heartbeat | `{"status": "healthy"}` |

---

## 🧪 Automated Testing

Run the automated unittest suite:

```bash
python tests/test_app.py
```

Output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.325s

OK (100% Pass)
```

---

## 💼 Portfolio & Interview Showcase Highlights

* **Software Architecture**: Clean modular separation across Controller, Service, ORM Database, and ML Inference layers.
* **DevOps Engineering**: Multi-stage Docker deployment, Docker Compose orchestration, and GitHub Actions CI pipelines.
* **ML Best Practices**: Automated scaling via `StandardScaler`, cross-validated benchmarking, F1 Score selection, and joblib serialization.
* **UI/UX Craftsmanship**: Dual Theme Dark/Light Mode, Toast Notifications, Floating Action Buttons, Skeleton Loading States, and 6 Chart.js visualizations.

---

## 📄 License
This project is licensed under the **MIT License** — suitable for technical portfolios, software engineering interviews, and open-source demonstration.
