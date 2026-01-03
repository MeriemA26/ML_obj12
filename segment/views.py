import os
import joblib
import numpy as np
from django.shortcuts import render

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'segment', 'ml', 'svm_segment_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'segment', 'ml', 'scaler_segment.pkl')

# Load model and scaler
svm_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# Features expected by scaler
FEATURES = ['MEDHHINC10', 'Unemployment_Rate_county', 'Labor_Force', 'Employed', 'Unemployed', 'median_household_income']

# Human-readable labels
FEATURE_CONFIG = {
    'MEDHHINC10': {'label': 'Median Household Income', 'example': 50000},
    'Unemployment_Rate_county': {'label': 'Unemployment Rate (%)', 'example': 5.0},
    'Labor_Force': {'label': 'Labor Force (count)', 'example': 100000},
    'Employed': {'label': 'Employed (count)', 'example': 95000},
    'Unemployed': {'label': 'Unemployed (count)', 'example': 5000},
    'median_household_income': {'label': 'Median Income (alt)', 'example': 52000},
}


def predict_segment(request):
    """Customer segmentation prediction using SVM."""
    result = None
    
    # Prepare features for template
    features_for_template = []
    for f in FEATURES:
        cfg = FEATURE_CONFIG.get(f, {})
        features_for_template.append({
            'name': f,
            'label': cfg.get('label', f),
            'example': cfg.get('example', 0)
        })
    
    if request.method == 'POST':
        try:
            # Get values from form
            values = []
            for f in FEATURES:
                val = float(request.POST.get(f, 0))
                values.append(val)
            
            # Scale and predict
            X = np.array(values).reshape(1, -1)
            X_scaled = scaler.transform(X)
            prediction = svm_model.predict(X_scaled)[0]
            result = int(prediction)
            
        except Exception as e:
            print(f"Segmentation error: {e}")
            result = None
    
    return render(request, 'segment/predict_segment.html', {
        'features': features_for_template,
        'result': result
    })
