# ============================================================
# Power BI Python Script for Diabetes Risk Prediction
# ============================================================
# INSTRUCTIONS:
# 1. Add a Python Visual to your Power BI report.
# 2. Drag these fields into the "Values" section:
#    - adult_obesity_rate
#    - physical_inactivity_rate
#    - food_environment_index
#    - POVRATE10 (Poverty Rate)
#    - MEDHHINC10 (Median Income)
#    - food_insecurity_rate
#    - SNAP_PART_RATE10
#    - access_to_exercise_pct
#    - uninsured_rate
#    - FIPS (or any other ID column to keep rows distinct)
# 3. Paste this entire script into the Python script editor in Power BI.
# 4. UPDATE THE 'model_path' AND 'scaler_path' VARIABLES BELOW
#    to point to where your .pkl files are located on your disk.
# ============================================================

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION - UPDATE THESE PATHS!
# ============================================================
# NOTE: Use forward slashes (/) or double backslashes (\\)
# Example: "C:/Users/YourName/Documents/diabetes_svm_model.pkl"
model_path = r"D:\app\Mizania+ v2\DATAWAREHOUSING\ML_obj12\diabetes_risk\ml_models\diabetes_svm_model (1).pkl"
scaler_path = r"D:\app\Mizania+ v2\DATAWAREHOUSING\ML_obj12\diabetes_risk\ml_models\diabetes_scaler (1).pkl"

# ============================================================
# DATA LOADING & PREPARATION
# ============================================================
# Power BI automatically loads selected fields into 'dataset'
# Create a copy to avoid SettingWithCopy warnings
if 'dataset' in locals():
    df = dataset.copy()
else:
    # Fallback for testing outside Power BI
    print("Warning: 'dataset' not found. Creating dummy data for testing.")
    df = pd.DataFrame({
        'adult_obesity_rate': [30, 35, 25],
        'physical_inactivity_rate': [25, 30, 20],
        'food_environment_index': [7, 5, 8],
        'POVRATE10': [15, 25, 10],
        'MEDHHINC10': [50000, 35000, 75000],
        'food_insecurity_rate': [12, 20, 8],
        'SNAP_PART_RATE10': [10, 15, 5],
        'access_to_exercise_pct': [65, 40, 85],
        'uninsured_rate': [12, 18, 8]
    })

# Map Power BI column names to model feature names
# Adjust these mappings if your Power BI column names are different
column_mapping = {
    'POVRATE10': 'poverty_rate',
    'MEDHHINC10': 'median_household_income',
    'SNAP_PART_RATE10': 'snap_participation_rate'
}
df_mapped = df.rename(columns=column_mapping)

# Ensure all 18 required features exist with correct names
required_features = [
    'adult_obesity_rate', 'physical_inactivity_rate', 'access_to_exercise_pct',
    'median_household_income', 'POVRATE10', 'food_insecurity_rate',
    'PCT_SNAP14', 'PCT_NSLP14', 'FFRPTH12', 'SUPERCPTH12', 
    'LACCESS_LOWI10', 'uninsured_rate', 'primary_care_physicians_per_100k',
    'PCT_65OLDER10', 'MEDHHINC10', 'SODA_PRICE10', 'MILK_PRICE10', 'RECFACPTH12'
]

# Default values for features that might not be in the dataset
# Default values for features that might not be in the dataset
# Using training data means to avoid biasing the prediction
feature_defaults = {
    'adult_obesity_rate': 0.30,      # Mean ~0.37
    'physical_inactivity_rate': 0.25, # Mean ~0.30
    'access_to_exercise_pct': 0.65,   # Mean ~0.46
    'median_household_income': 50000, # Mean ~60k
    'POVRATE10': 15.0,                # Mean ~19.7
    'food_insecurity_rate': 0.12,     # Mean ~0.13
    'PCT_SNAP14': 12.0,               # Mean ~16.2
    'PCT_NSLP14': 10.15,              # Mean ~10.1 (CRITICAL FIX)
    'FFRPTH12': 0.6,                  # Mean ~0.6
    'SUPERCPTH12': 0.01,              # Mean ~0.01
    'LACCESS_LOWI10': 16500.0,        # Mean ~16504 (Count, not %)
    'uninsured_rate': 0.12,           # Mean ~0.11
    'primary_care_physicians_per_100k': 41.5, # Mean ~41.5
    'PCT_65OLDER10': 14.5,            # Mean ~14.5
    'MEDHHINC10': 40838.0,            # Mean ~40838
    'SODA_PRICE10': 2.55,             # Mean ~2.55
    'MILK_PRICE10': 2.57,             # Mean ~2.57
    'RECFACPTH12': 0.04               # Mean ~0.04
}

# Create a working dataframe with all required columns
X = pd.DataFrame(index=df.index)

for feat in required_features:
    if feat in df_mapped.columns:
        # Use mapped column if it exists
        X[feat] = df_mapped[feat]
    elif feat == 'MEDHHINC10' and 'median_household_income' in df_mapped.columns:
        # Special mapping for the duplicate income field
        X[feat] = df_mapped['median_household_income']
    else:
        # Use default value
        X[feat] = feature_defaults.get(feat, 0)

# Fill any remaining NaNs
X = X.fillna(X.median()).fillna(0)

# ============================================================
# LOAD MODEL & PREDICT
# ============================================================
try:
    # Load model and scaler
    svm_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # 1. Scale features
    # Ensure columns are in the exact order expected by the model
    X = X[required_features]
    
    # UNIT CONVERSION:
    # Model expects decimals (0.0-1.0) for some rates, but Power BI might provide percentages (0-100)
    decimal_fields = [
        'adult_obesity_rate', 
        'physical_inactivity_rate', 
        'access_to_exercise_pct', 
        'food_insecurity_rate', 
        'uninsured_rate'
    ]
    
    for field in decimal_fields:
        # Apply conversion only if values look like percentages (mean > 1.0)
        if field in X.columns and X[field].mean() > 1.0:
            X[field] = X[field] / 100.0

    X_scaled = scaler.transform(X)
    
    # 2. Predict Probability
    # predict_proba returns [prob_class_0, prob_class_1]
    probabilities = svm_model.predict_proba(X_scaled)[:, 1]
    
    # 3. Predict Class
    predictions = svm_model.predict(X_scaled)
    
    # Add results back to original dataframe
    df['Risk_Probability'] = probabilities
    df['Predicted_Risk_LeveL'] = predictions
    
    # Create descriptive labels
    df['Risk_Category'] = df['Risk_Probability'].apply(
        lambda x: 'High Risk' if x >= 0.20 else ('Medium Risk' if x >= 0.10 else 'Low Risk')
    )
    
    # Create a nice visualization
    # Bar chart of Risk Categories
    plt.figure(figsize=(10, 6))
    
    # Count the categories
    counts = df['Risk_Category'].value_counts()
    
    # Ensure all categories are represented even if count is 0
    for cat in ['Low Risk', 'Medium Risk', 'High Risk']:
        if cat not in counts:
            counts[cat] = 0
            
    # Sort them logically
    categories = ['Low Risk', 'Medium Risk', 'High Risk']
    values = [counts.get(cat, 0) for cat in categories]
    colors = ['green', 'orange', 'red']
    
    # Create bar plot
    bars = plt.bar(categories, values, color=colors)
    
    plt.title('Diabetes Risk Distribution (Predicted by SVM)', fontsize=16)
    plt.xlabel('Risk Category', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add counts on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=11)
        
    plt.tight_layout()
    plt.show()
    
except Exception as e:
    error_msg = f"Error: {str(e)}"
    print(error_msg)
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, f"An error occurred:\n{error_msg}\n\nCheck your file paths!", 
             ha='center', va='center', fontsize=12, color='red', wrap=True)
    plt.axis('off')
    plt.show()
