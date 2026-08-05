# 🏥 Smart Health Prediction System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Project Overview

**Smart Health Prediction System** is a full-stack clinical risk evaluation and population health analytics platform. Designed using standard software engineering practices, the system integrates a **Python/Flask REST API**, **SQLAlchemy ORM database engine**, **Docker containerization**, **GitHub Actions CI/CD**, and a multi-model **Machine Learning pipeline** (Random Forest Ensemble, Logistic Regression, Decision Tree) optimized for low-latency risk evaluation across 5 critical medical conditions.

The platform provides healthcare professionals with diagnostic risk scores, calculated health indexes (0–100), key risk factor interpretability, lifestyle recommendations, downloadable clinical PDF reports with QR verification, and interactive Chart.js analytics dashboards.

---

## 🎯 Project Objectives

- Predict disease risk using machine learning algorithms
- Provide an interactive healthcare dashboard for clinicians
- Store and manage patient prediction history
- Generate downloadable clinical PDF reports
- Visualize population health analytics

---

## ✨ Key Features

* **⚡ Low-Latency AI Risk Assessment**: Evaluates 14 clinical vitals in real time (< 20ms execution latency).
* **🎯 Multi-Disease Risk Evaluation**: Simultaneous probability scoring for Heart Disease, Diabetes, Chronic Kidney Disease, Stroke Risk, and Hypertension.
* **🎨 Modern Glassmorphic Interface**: Dual-theme UI (Clinical Light & Dark AI Mode) with dynamic CSS variables and skeleton loading overlays.
* **📊 Population Health Analytics Studio**: 6 interactive Chart.js visual dashboards tracking prevalence distributions, monthly trends, and SLA telemetry.
* **🏥 Printable Clinical Diagnostic Reports**: Generates formal PDF/HTML diagnostic reports complete with hospital letterhead, vitals matrix, ML model lineage, and QR verification badges.
* **🗄️ Indexed Patient Records History**: Supports multi-criteria filtering, search, interactive column header sorting, and CSV data stream exports.
* **🏷️ Pipeline & Model Versioning**: Dynamic tracking of model version (`v2.0.1`), dataset version (`Smart Health Dataset v1.2`), training execution duration (`3.36s`), and training timestamps.
* **🐳 Docker Ready**: Multi-stage Docker containerization, Docker Compose orchestration, and automated GitHub Actions CI testing.

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Flask |
| **Database** | SQLite |
| **Machine Learning** | Scikit-learn |
| **Frontend** | HTML, CSS, JavaScript |
| **Charts** | Chart.js |
| **Reports** | ReportLab |
| **Containerization** | Docker |
| **Testing** | unittest |

---

## 🧠 Machine Learning Pipeline

```text
Smart Health Synthetic Dataset v1.2 (10,500 Records)
           ↓
Data Preprocessing & Feature Engineering (14 Clinical Vitals)
           ↓
Train / Test Stratified Split (8,400 Train / 2,100 Test)
           ↓
Feature Normalization (StandardScaler Pipeline)
           ↓
Multi-Model Training & Benchmarking (Random Forest, Logistic Regression, Decision Tree)
           ↓
Model Serialization (joblib: scaler.joblib & random_forest.joblib)
           ↓
Flask REST API Real-Time Inference (< 20ms Latency)
           ↓
SQLAlchemy ORM Audit Logging & Visual Analytics Studio
```

---

## 📊 Dataset Information

The system is trained and benchmarked on the **Smart Health Synthetic Dataset v1.2**, built from standardized clinical reference bounds across 10,500 patient cohorts:

* **Total Records**: 10,500 patient profiles
* **Train / Test Ratio**: 80% Training (8,400 samples) / 20% Evaluation Holdout (2,100 samples)
* **Clinical Features (14)**: Age, Gender, Height (cm), Weight (kg), BMI, Systolic BP, Diastolic BP, Fasting Glucose, Serum Cholesterol, Resting Heart Rate, Smoking History, Alcohol Consumption, Physical Activity, and Family History.
* **Target Classes**: 3 Risk Levels (`Low`, `Medium`, `High`) mapped across 5 specific disease probabilities.

---

## 🏗️ System Architecture

```text
Client Browser (HTML5 / Vanilla CSS / ES6 JS / Chart.js)
           │
           │ HTTP / REST API (JSON)
           ▼
Flask 3.0 Application Server (app.py)
   ├── Latency Middleware (@before_request / @after_request)
   ├── Routing & JSON Serialization
   ├── HealthPredictor Engine (ml/predictor.py)
   │     ├── StandardScaler (joblib)
   │     └── Classifiers (Random Forest, LR, DT)
   ├── SQLAlchemy ORM Layer (database/models.py)
   │     └── SQLite Database (database/medpredict.db)
   └── Clinical Report Generator (reports/generator.py)
```

---

## 🔄 Application Workflow

1. **Vitals Input**: User inputs patient demography, vitals, lifestyle habits, and selects a classifier model (or clicks *Generate Random Demo Data*).
2. **Preprocessing**: Frontend validates Systolic BP > Diastolic BP; backend normalizes features using `StandardScaler`.
3. **Inference Execution**: Selected Scikit-learn model evaluates multi-label probabilities in < 20 ms.
4. **Outcome Rendering**: Interface displays SVG Circular Risk Gauge, Health Score (0–100), 5 Disease Probability meters, Key Risk Drivers, and Lifestyle Guidance.
5. **Database Logging**: Prediction metrics and system response latency are saved to SQLite via SQLAlchemy ORM.
6. **Report Generation**: Users can download PDF diagnostic reports with embedded QR verification badges or export history CSVs.

---

## 📁 Project Folder Structure

```text
Smart-Health-Prediction-System/
├── 📁 .github/
│   └── 📁 workflows/
│       └── ci.yml             # GitHub Actions CI Workflow Pipeline
├── app.py                     # Flask REST API Controller & Route Handlers
├── config.py                  # Environment Configuration & Path Directory Manager
├── Dockerfile                 # Multi-Stage Docker Build
├── docker-compose.yml         # Container Orchestration Specification
├── .env.example               # Environment Variables Template
├── .gitignore                 # Version Control Exclusions
├── LICENSE                    # MIT License
├── requirements.txt            # Python Dependencies Specification
├── README.md                  # Comprehensive Documentation
├── 📁 database/
│   ├── db.py                  # Database Connection & Automated Seeder (520+ Records)
│   ├── models.py              # Patient, Prediction, ModelMetric, ReportLog Schemas
│   └── medpredict.db          # SQLite Database Storage File
├── 📁 datasets/
│   ├── generate_dataset.py    # 10,500 Clinical Dataset Generator Script
│   └── medpredict_10k.csv     # Serialized Training Dataset
├── 📁 demo/
│   └── README.md              # Demonstration Video Guide & Assets
├── 📁 ml/
│   ├── trainer.py             # Model Training, Cross-Validation & Metric Serializer
│   └── predictor.py           # Real-Time Multi-Disease Risk Inference Engine
├── 📁 reports/
│   └── generator.py           # Printable PDF/HTML Clinical Exporter & CSV Data Streamer
├── 📁 screenshots/
│   └── README.md              # Screenshots Repository Guide
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css          # Glassmorphic Design System & Dual-Theme CSS
│   └── 📁 js/
│       ├── main.js            # Core App Controller & Input Validator
│       ├── toast.js           # Floating Toast Notification Engine
│       ├── charts.js          # 6-Chart Visual Dashboard Controller
│       └── admin.js           # History Table & Dynamic Metrics Binding
├── 📁 templates/
│   └── index.html             # Consolidated Dashboard Single-Page HTML
├── 📁 trained_models/
│   └── metrics.json           # Serialized Model Metrics & Versioning Data
└── 📁 tests/
    └── test_app.py            # Automated Unittest Suite (8/8 Passed)
```

---

## 🚀 Installation Guide

### Requirements

* **Python**: `3.12+`
* **Pip**: `23.0+`
* **Docker** *(Optional)*: `24.0+` & Docker Compose `v2+`

### Running the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dvharshavardhan/Smart-Health-Prediction-System.git
   cd Smart-Health-Prediction-System
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database & Train Models** *(Optional - Pre-bundled)*:
   ```bash
   python ml/trainer.py
   ```

5. **Start the Flask Application**:
   ```bash
   python app.py
   ```

6. **Access the Web Dashboard**:
   Open browser at `http://127.0.0.1:5000`

---

### Docker Deployment

Run containerized using Docker Compose:

```bash
docker compose up -d
```

Access the platform at: `http://localhost:5000`

To build manually:
```bash
docker build -t smart-health-prediction:latest .
docker run -d -p 5000:5000 --name health_app smart-health-prediction:latest
```

---

## 📡 REST API Documentation

| Endpoint | Method | Description | Content-Type | Status Code |
| :--- | :---: | :--- | :---: | :---: |
| `GET /` | `GET` | Renders main web application dashboard | `text/html` | `200 OK` |
| `POST /api/predict` | `POST` | Executes real-time multi-disease risk prediction | `application/json` | `200 OK` |
| `GET /api/patients` | `GET` | Paginated search, multi-filter & column-sorted patient logs | `application/json` | `200 OK` |
| `GET /api/analytics` | `GET` | Population health analytics & dynamic dataset metadata | `application/json` | `200 OK` |
| `GET /api/models/metrics` | `GET` | ML classifier performance metrics & benchmarking | `application/json` | `200 OK` |
| `GET /api/reports` | `GET` | Diagnostic reports counter & audit trail logs | `application/json` | `200 OK` |
| `GET /api/system/status` | `GET` | Live telemetry (database, models, latency, speed) | `application/json` | `200 OK` |
| `GET /api/reports/export/<id>` | `GET` | Downloads printable PDF/HTML clinical report | `text/html` | `200 OK` |
| `GET /api/reports/csv_export` | `GET` | Streams patient history dataset as CSV file | `text/csv` | `200 OK` |
| `DELETE /api/prediction/<id>` | `DELETE` | Removes patient prediction record from database | `application/json` | `200 OK` |
| `GET /api/health` | `GET` | Heartbeat & SLA verification status | `application/json` | `200 OK` |

---

## 📸 Project Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Prediction
![Prediction](screenshots/prediction.png)

### Analytics
![Analytics](screenshots/analytics.png)

### History
![History](screenshots/history.png)

### Reports
![Reports](screenshots/report.png)

---

## 🎥 Demo Video

Watch the complete demonstration video here:

*(Coming Soon — Video demonstration link will be added upon upload)*

---

## 🧪 Testing

The platform includes an automated unittest suite verifying REST API routes, SLA compliance boundaries (< 1000ms), database ORM persistence, and ML model inference consistency:

```bash
python tests/test_app.py
```

**Output**:
```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.534s

OK (100% Pass Rate)
```

---

## ⚡ Performance

* **Average Inference Latency**: `14.2 ms` (Scikit-Learn Random Forest)
* **API Response SLA**: `< 1,000 ms` Target (100% SLA Compliance Rate)
* **Database Query Performance**: Indexed columns on `patient_code`, `risk_level`, and `created_at`
* **Frontend Responsiveness**: CSS Grid / Flexbox layout with smooth transitions

---

## 📄 Reports

The platform features an automated clinical report generator producing diagnostic summaries:
* **QR Code Verification**: Includes embedded `QR VERIFIED OFFICIAL` badge.
* **Patient Vitals Matrix**: Clinical measurements mapped against normal reference ranges.
* **ML Lineage Table**: Documents model version (`v2.0.1`), classifier type, train/test split, and inference SLA.
* **Legal Disclaimer & Signature**: Includes physician signature lines and institutional disclaimers.

---

## 📈 Analytics Dashboard

The **Analytics & ML Studio** tab aggregates population health insights into 6 visual Chart.js dashboards:
1. **5 Diseases Prevalence Donut Chart**: Proportional risk across Heart Disease, Diabetes, Kidney Disease, Stroke Risk, and Hypertension.
2. **Risk Category Pie Chart**: High, Medium, and Low risk population distribution.
3. **Monthly Evaluations Line Chart**: Longitudinal patient screening volume trends.
4. **Demographics Bar Chart**: Age group and gender risk breakdown.
5. **Execution Latency SLA Line Chart**: Real-time request response time vs 1,000ms SLA ceiling.
6. **ML Classifier Comparison Bar Chart**: Side-by-side Accuracy, Precision, Recall, and F1 Score evaluation.

---

## 🤖 Machine Learning Models

Three supervised classification algorithms were trained and benchmarked on 10,500 patient records:

| Model Architecture | Accuracy (%) | Precision (%) | Recall (%) | F1 Score (%) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Classifier (Primary)** | **88.50%** | **87.90%** | **88.20%** | **88.05%** | **Primary Best** |
| **Logistic Regression** | 84.20% | 83.50% | 84.10% | 83.80% | Operational |
| **Decision Tree Classifier** | 79.50% | 79.10% | 79.40% | 79.25% | Operational |

---

## 🗄️ Database Design

The relational database is powered by **SQLite** and managed via **SQLAlchemy ORM**:

* **`patients`**: Stores demographic attributes (`patient_code`, `name`, `age`, `gender`, `height_cm`, `weight_kg`, `bmi`).
* **`predictions`**: Stores 14 clinical vitals, risk level, confidence percentage, JSON disease probabilities, JSON risk factors, recommendations, model used, and response latency.
* **`model_metrics`**: Stores serialized benchmark metrics for classifier architectures.
* **`reports`**: Stores audit logs for generated PDF and CSV diagnostic exports.
* **`system_metrics`**: Stores per-request API latency measurements and SLA compliance indicators.

---

## 🔮 Future Enhancements

* [ ] Integration with HL7 FHIR standards for EHR interoperability.
* [ ] Support for Deep Learning Neural Network models (PyTorch / TensorFlow).
* [ ] Real-time WebSocket streaming for continuous ICU patient vital monitoring.
* [ ] OAuth2 / OpenID Connect multi-tenant authentication for hospital networks.

---

## 💼 Resume Highlights

- Flask REST APIs
- Machine Learning Integration
- SQLAlchemy ORM
- Docker
- GitHub Actions
- Interactive Dashboard
- PDF Reports
- Chart.js Analytics

---

## 🗣️ Interview Talking Points

* **Handling Multi-Disease Risk**: *"Rather than predicting a single binary condition, the platform maps 14 normalized clinical vitals across 5 distinct disease probability distributions using standardized feature scaling."*
* **Low-Latency Inference**: *"Inference execution latency is tracked via Flask request middleware and logged into a telemetry table, verifying that predictions fulfill the sub-1-second SLA target."*
* **SQLAlchemy ORM & Database Seeding**: *"The database schema maintains clear relational separation between patient profiles, prediction logs, model metrics, report audit trails, and system telemetry, pre-seeded with 520+ realistic historical records."*
* **Dynamic Pipeline Metadata**: *"Dataset versioning, model versioning (v2.0.1), training duration, and timestamps are dynamically bound from `metrics.json` directly to the REST API and dashboard UI."*

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Harsha Vardhan**
* **GitHub**: [https://github.com/dvharshavardhan](https://github.com/dvharshavardhan)
* **LinkedIn**: [https://linkedin.com/in/dvharshavardhan](https://linkedin.com/in/dvharshavardhan)
