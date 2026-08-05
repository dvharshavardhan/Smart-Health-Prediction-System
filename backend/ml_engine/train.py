import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from dataset_generator import generate_healthcare_dataset

def train_and_evaluate():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'data')
    models_dir = os.path.join(base_dir, 'backend', 'ml_engine', 'models')
    charts_dir = os.path.join(base_dir, 'static', 'charts')
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, 'healthcare_records_10k.csv')
    if not os.path.exists(csv_path):
        print("Dataset not found. Generating 10,500 healthcare records...")
        df = generate_healthcare_dataset(10500, output_path=csv_path)
    else:
        df = pd.read_csv(csv_path)
        print(f"Loaded existing dataset with {len(df)} records.")
        
    feature_cols = [
        'age', 'gender_code', 'systolic_bp', 'diastolic_bp', 
        'bmi', 'glucose_level', 'cholesterol', 
        'smoking_status', 'physical_activity', 'heart_rate', 'family_history'
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
    
    # Model 2: Decision Tree
    dt_model = DecisionTreeClassifier(max_depth=6, random_state=42)
    dt_model.fit(X_train_scaled, y_train)
    dt_preds = dt_model.predict(X_test_scaled)
    
    # Model 3: Random Forest Classifier (Primary Ensemble)
    rf_model = RandomForestClassifier(n_estimators=120, max_depth=10, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    rf_preds = rf_model.predict(X_test_scaled)
    
    def compute_metrics(y_true, y_pred):
        return {
            'accuracy': float(np.round(accuracy_score(y_true, y_pred), 4)),
            'precision': float(np.round(precision_score(y_true, y_pred, average='weighted'), 4)),
            'recall': float(np.round(recall_score(y_true, y_pred, average='weighted'), 4)),
            'f1_score': float(np.round(f1_score(y_true, y_pred, average='weighted'), 4)),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        
    metrics = {
        'logistic_regression': compute_metrics(y_test, lr_preds),
        'decision_tree': compute_metrics(y_test, dt_preds),
        'random_forest': compute_metrics(y_test, rf_preds),
        'dataset_size': len(df),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'feature_cols': feature_cols
    }
    
    # Save trained artifacts
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.joblib'))
    joblib.dump(lr_model, os.path.join(models_dir, 'logistic_regression.joblib'))
    joblib.dump(dt_model, os.path.join(models_dir, 'decision_tree.joblib'))
    joblib.dump(rf_model, os.path.join(models_dir, 'random_forest.joblib'))
    
    with open(os.path.join(models_dir, 'metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
        
    # Generate Feature Importance Plot for Random Forest
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_features = [feature_cols[i] for i in indices]
    sorted_importances = importances[indices]
    
    plt.figure(figsize=(10, 5))
    plt.barh(sorted_features[::-1], sorted_importances[::-1], color='#3b82f6')
    plt.title('Random Forest - Feature Importance Analysis')
    plt.xlabel('Relative Importance Weight')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'feature_importance.png'), dpi=200)
    plt.close()
    
    # Model Comparison Chart
    models_names = ['Logistic Regression', 'Decision Tree', 'Random Forest']
    accuracies = [metrics['logistic_regression']['accuracy'] * 100,
                  metrics['decision_tree']['accuracy'] * 100,
                  metrics['random_forest']['accuracy'] * 100]
    
    plt.figure(figsize=(8, 4.5))
    bars = plt.bar(models_names, accuracies, color=['#94a3b8', '#60a5fa', '#10b981'])
    plt.ylim(60, 100)
    plt.ylabel('Accuracy (%)')
    plt.title('ML Model Accuracy Benchmarking')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.8, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'model_accuracy_comparison.png'), dpi=200)
    plt.close()
    
    print("\n================ ML Training Complete ================")
    print(f"Dataset Records: {len(df)}")
    print(f"Logistic Regression Accuracy: {metrics['logistic_regression']['accuracy'] * 100:.2f}%")
    print(f"Decision Tree Accuracy:       {metrics['decision_tree']['accuracy'] * 100:.2f}%")
    print(f"Random Forest Accuracy:       {metrics['random_forest']['accuracy'] * 100:.2f}% (TARGET ~85%)")
    print("======================================================\n")
    
    return metrics

if __name__ == '__main__':
    train_and_evaluate()
