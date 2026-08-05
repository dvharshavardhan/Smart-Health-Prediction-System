import os
import sys
import time
import json
import joblib
from datetime import datetime
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from datasets.generate_dataset import generate_medical_dataset
from config import Config

def train_and_benchmark():
    """
    Trains, benchmarks, and serializes Logistic Regression, Decision Tree, and Random Forest models.
    Measures training duration and stores Model & Dataset Versioning metadata.
    """
    start_time = time.time()
    
    dataset_path = os.path.join(Config.DATASETS_DIR, 'medpredict_10k.csv')
    if not os.path.exists(dataset_path):
        print("Generating 10,500 patient dataset...")
        df = generate_medical_dataset(10500, output_path=dataset_path)
    else:
        df = pd.read_csv(dataset_path)
        print(f"Loaded existing dataset with {len(df)} records.")
        
    feature_cols = [
        'age', 'gender_code', 'height_cm', 'weight_kg', 'bmi', 
        'systolic_bp', 'diastolic_bp', 'glucose', 'cholesterol', 
        'heart_rate', 'smoking', 'alcohol', 'exercise', 'family_history'
    ]
    
    X = df[feature_cols]
    y = df['health_risk_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model 1: Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    lr_preds = lr_model.predict(X_test_scaled)
    
    # Model 2: Decision Tree Classifier
    dt_model = DecisionTreeClassifier(max_depth=7, random_state=42)
    dt_model.fit(X_train_scaled, y_train)
    dt_preds = dt_model.predict(X_test_scaled)
    
    # Model 3: Random Forest Classifier (Primary Ensemble)
    rf_model = RandomForestClassifier(n_estimators=130, max_depth=10, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    rf_preds = rf_model.predict(X_test_scaled)
    
    training_duration_sec = round(time.time() - start_time, 2)
    
    def compute_metrics(y_true, y_pred):
        return {
            'accuracy': float(np.round(accuracy_score(y_true, y_pred), 4)),
            'precision': float(np.round(precision_score(y_true, y_pred, average='weighted'), 4)),
            'recall': float(np.round(recall_score(y_true, y_pred, average='weighted'), 4)),
            'f1_score': float(np.round(f1_score(y_true, y_pred, average='weighted'), 4)),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        
    now = datetime.utcnow()
    metrics = {
        'logistic_regression': compute_metrics(y_test, lr_preds),
        'decision_tree': compute_metrics(y_test, dt_preds),
        'random_forest': compute_metrics(y_test, rf_preds),
        'model_version': 'v2.0.1',
        'dataset_version': 'MedPredict Dataset v1.2',
        'dataset_name': 'MedPredict Synthetic Clinical Dataset',
        'dataset_size': len(df),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'feature_cols': feature_cols,
        'training_duration_sec': training_duration_sec,
        'trained_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'trained_at_display': now.strftime('%d-%b-%Y')
    }
    
    # Determine best model based on F1 Score
    best_model_name = 'random_forest'
    best_f1 = metrics['random_forest']['f1_score']
    if metrics['logistic_regression']['f1_score'] > best_f1:
        best_model_name = 'logistic_regression'
        best_f1 = metrics['logistic_regression']['f1_score']
    if metrics['decision_tree']['f1_score'] > best_f1:
        best_model_name = 'decision_tree'
        
    metrics['best_model'] = best_model_name
    
    # Save artifacts
    joblib.dump(scaler, os.path.join(Config.MODELS_DIR, 'scaler.joblib'))
    joblib.dump(lr_model, os.path.join(Config.MODELS_DIR, 'logistic_regression.joblib'))
    joblib.dump(dt_model, os.path.join(Config.MODELS_DIR, 'decision_tree.joblib'))
    joblib.dump(rf_model, os.path.join(Config.MODELS_DIR, 'random_forest.joblib'))
    
    with open(os.path.join(Config.MODELS_DIR, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
        
    print("\n================ MedPredict AI Training Complete ================")
    print(f"Model Version:         {metrics['model_version']}")
    print(f"Dataset Version:       {metrics['dataset_version']}")
    print(f"Training Duration:     {metrics['training_duration_sec']} sec")
    print(f"Dataset Records:       {len(df)}")
    print(f"Training Timestamp:    {metrics['trained_at']}")
    print(f"Logistic Regression:   {metrics['logistic_regression']['accuracy'] * 100:.2f}%")
    print(f"Decision Tree:         {metrics['decision_tree']['accuracy'] * 100:.2f}%")
    print(f"Random Forest:         {metrics['random_forest']['accuracy'] * 100:.2f}% (BEST MODEL)")
    print("=================================================================\n")
    
    return metrics

if __name__ == '__main__':
    train_and_benchmark()
