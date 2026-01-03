# ============================================================
# SVM Classification Script for Power BI
# Copy this script into Power BI's Python script editor
# ============================================================
# 'dataset' contient les données d'entrée pour ce script

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Use the dataset from Power BI
df = dataset.copy()

# ===========================================
# 1. CREATE TARGET VARIABLE (Diabetes Risk)
# ===========================================
if 'diabetes_prevalence_rate' in df.columns:
    diabetes_col = 'diabetes_prevalence_rate'
elif 'PCT_DIABETES_ADULTS10' in df.columns:
    diabetes_col = 'PCT_DIABETES_ADULTS10'
else:
    raise ValueError("No diabetes column found")

# Create binary target based on median
median_val = df[diabetes_col].median()
df['diabetes_risk'] = (df[diabetes_col] > median_val).astype(int)

# ===========================================
# 2. SELECT FEATURES
# ===========================================
feature_candidates = [
    'adult_obesity_rate', 'physical_inactivity_rate', 
    'food_environment_index', 'POVRATE10', 'MEDHHINC10',
    'food_insecurity_rate', 'SNAP_PART_RATE10', 
    'access_to_exercise_pct', 'uninsured_rate'
]
features = [f for f in feature_candidates if f in df.columns]

# Clean data - remove rows with missing values
df_clean = df[features + ['diabetes_risk']].dropna()

# ===========================================
# 3. PREPARE DATA
# ===========================================
X = df_clean[features]
y = df_clean['diabetes_risk']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===========================================
# 4. TRAIN SVM MODEL (with downsampling for speed)
# ===========================================
np.random.seed(42)
if len(X_scaled) > 15000:
    idx = np.random.choice(len(X_scaled), 15000, replace=False)
    X_train_fit = X_scaled[idx]
    y_train_fit = y.iloc[idx]
else:
    X_train_fit = X_scaled
    y_train_fit = y

# Train SVM
svm_model = SVC(kernel='rbf', probability=True, random_state=42, C=1.0, gamma='scale')
svm_model.fit(X_train_fit, y_train_fit)

# ===========================================
# 5. PREDICTIONS ON ALL DATA
# ===========================================
df_clean['Risk_Probability'] = svm_model.predict_proba(X_scaled)[:, 1]
df_clean['Risk_Category'] = df_clean['Risk_Probability'].apply(
    lambda x: 'High Risk' if x > 0.7 else ('Medium Risk' if x > 0.4 else 'Low Risk')
)

# Predicted_Risk as a numeric value (1 for High/Medium, 0 for Low) for metrics
df_clean['Predicted_Risk'] = (df_clean['Risk_Probability'] > 0.5).astype(int)

# Add a helper column for counting in Power BI visuals
# This avoids the "Sum of Predicted_Risk" issue in charts
df_clean['Case_Count'] = 1

# ===========================================
# 6. MODEL METRICS
# ===========================================
accuracy = accuracy_score(y, df_clean['Predicted_Risk'])
precision = precision_score(y, df_clean['Predicted_Risk'])
recall = recall_score(y, df_clean['Predicted_Risk'])
f1 = f1_score(y, df_clean['Predicted_Risk'])

# Add metrics as columns for Power BI
df_clean['Model_Accuracy'] = accuracy
df_clean['Model_Precision'] = precision
df_clean['Model_Recall'] = recall
df_clean['Model_F1_Score'] = f1

# Output the result for Power BI
# Power BI will use df_clean as the output table
