import os
import json
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, 'ml')

# Feature labels mapping (technical name -> readable name)
FEATURE_LABELS = {
    'SUPERC12': 'Supercenters Count',
    'LACCESS_HHNV10': 'Households Without Vehicle',
    'Employed': 'Employed Population',
    'Labor_Force': 'Labor Force Size',
    'FFR12': 'Fast Food Restaurants',
    'FSR12': 'Full-Service Restaurants',
    'GROC12': 'Grocery Stores Count',
    'Unemployed': 'Unemployed Population',
    'PCT_HISP10': 'Hispanic Population %',
    'SNAP_PART_RATE10': 'SNAP Participation Rate %',
    'PCT_NHWHITE10': 'Non-Hispanic White %',
    'PCT_OBESE_ADULTS10': 'Adult Obesity Rate %',
    'PCT_WIC14': 'WIC Participation %',
    'access_to_exercise_pct': 'Exercise Access %',
    'median_household_income': 'Median Household Income ($)'
}

# Default values for testing (realistic US county averages)
FEATURE_DEFAULTS = {
    'SUPERC12': 2,
    'LACCESS_HHNV10': 500,
    'Employed': 25000,
    'Labor_Force': 30000,
    'FFR12': 15,
    'FSR12': 10,
    'GROC12': 8,
    'Unemployed': 2000,
    'PCT_HISP10': 15.0,
    'SNAP_PART_RATE10': 12.0,
    'PCT_NHWHITE10': 65.0,
    'PCT_OBESE_ADULTS10': 30.0,
    'PCT_WIC14': 8.0,
    'access_to_exercise_pct': 60.0,
    'median_household_income': 50000
}

# Load model and scaler once
try:
    model = joblib.load(os.path.join(ML_DIR, 'run_1_best_model_KNN.pkl'))
    scaler = joblib.load(os.path.join(ML_DIR, 'run_1_scaler.pkl'))
    
    with open(os.path.join(ML_DIR, 'run_1_model_info.json')) as f:
        model_info = json.load(f)
    
    FEATURES = model_info['feature_names']
    MODEL_LOADED = True
    print("✅ KNN Limited Access model loaded successfully!")
    print(f"   • Features: {len(FEATURES)}")
    print(f"   • Test R²: {model_info['performance_metrics']['test_r2']:.4f}")
except Exception as e:
    print(f"⚠️ Error loading KNN model: {e}")
    FEATURES = list(FEATURE_LABELS.keys())
    model_info = {}
    MODEL_LOADED = False


def predict_view(request):
    """Main prediction view for Limited Access Population"""
    prediction = None
    input_values = {}
    input_display = []  # List of tuples (label, value)
    prediction_context = None
    
    # Create fields list with label, name, and default
    fields = []
    for f in FEATURES:
        fields.append({
            'name': f,
            'label': FEATURE_LABELS.get(f, f),
            'default': FEATURE_DEFAULTS.get(f, 0)
        })
    
    if request.method == 'POST' and MODEL_LOADED:
        try:
            values = []
            for f in FEATURES:
                val = float(request.POST.get(f, FEATURE_DEFAULTS.get(f, 0)))
                values.append(val)
                input_values[f] = val
                input_display.append({
                    'label': FEATURE_LABELS.get(f, f),
                    'value': val
                })
            
            # Scale features
            X = np.array([values])
            X_scaled = scaler.transform(X)
            
            # Predict
            pred = model.predict(X_scaled)[0]
            prediction = f"{float(pred):,.0f}"
            
            # Add context based on prediction value
            pred_val = float(pred)
            if pred_val < 5000:
                prediction_context = {
                    'level': 'Low',
                    'color': 'success',
                    'message': 'This area has good food access for most residents.'
                }
            elif pred_val < 20000:
                prediction_context = {
                    'level': 'Moderate',
                    'color': 'warning',
                    'message': 'A moderate number of residents have limited food access. Consider targeted interventions.'
                }
            else:
                prediction_context = {
                    'level': 'High',
                    'color': 'danger',
                    'message': 'A significant population has limited food access. Urgent intervention recommended.'
                }
            
            print(f"🎯 KNN Prediction: {prediction} ({prediction_context['level']} limited access)")
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            import traceback
            traceback.print_exc()
            prediction = "Error"
    
    return render(
        request,
        'mlapp/index.html',
        {
            'fields': fields,
            'prediction': prediction,
            'prediction_context': prediction_context,
            'input_display': input_display,
            'model_type': 'KNN Regression',
        }
    )


def test_prediction(request):
    """API endpoint for testing predictions"""
    if not MODEL_LOADED:
        return JsonResponse({'error': 'Model not loaded'})
    
    values = [FEATURE_DEFAULTS.get(f, 0) for f in FEATURES]
    
    X = np.array([values])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]
    
    return JsonResponse({
        'prediction': float(pred),
        'features_used': {f: FEATURE_DEFAULTS.get(f, 0) for f in FEATURES}
    })
