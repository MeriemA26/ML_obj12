import os
import joblib
import numpy as np
from django.shortcuts import render

# Path to ml folder
ML_DIR = os.path.join(os.path.dirname(__file__), "ml")

# ============================================
# MODEL 1: RF Health Score Prediction
# ============================================
try:
    rf_scaler = joblib.load(os.path.join(ML_DIR, "rf_scaler.pkl"))
    rf_model = joblib.load(os.path.join(ML_DIR, "rf_model.pkl"))
    RF_LOADED = True
    print("✅ RF Health Score model loaded!")
except Exception as e:
    print(f"⚠️ RF model not loaded: {e}")
    RF_LOADED = False

RF_FEATURES = [
    'median_household_income', 'child_poverty_rate', 'physical_inactivity_rate',
    'food_access_score', 'POVRATE10', 'PCT_SNAP14', 'diabetes_prevalence_rate',
    'food_environment_index'
]

RF_FEATURE_LABELS = {
    'median_household_income': 'Median Household Income ($)',
    'child_poverty_rate': 'Child Poverty Rate (%)',
    'physical_inactivity_rate': 'Physical Inactivity Rate (%)',
    'food_access_score': 'Food Access Score',
    'POVRATE10': 'Poverty Rate (%)',
    'PCT_SNAP14': 'SNAP Participation (%)',
    'diabetes_prevalence_rate': 'Diabetes Prevalence (%)',
    'food_environment_index': 'Food Environment Index (0-10)'
}

RF_DEFAULTS = {
    'median_household_income': 50000,
    'child_poverty_rate': 20,
    'physical_inactivity_rate': 25,
    'food_access_score': 6,
    'POVRATE10': 15,
    'PCT_SNAP14': 12,
    'diabetes_prevalence_rate': 10,
    'food_environment_index': 7
}


# ============================================
# MODEL 2: Store Impact on Health (KNN)
# ============================================
try:
    knn_model = joblib.load(os.path.join(ML_DIR, "Store Impact on Health.pkl"))
    le = joblib.load(os.path.join(ML_DIR, "label_encoder_health.pkl"))
    store_scaler = joblib.load(os.path.join(ML_DIR, "scaler_features_health.pkl"))
    STORE_LOADED = True
    print("✅ Store Impact on Health model loaded!")
except Exception as e:
    print(f"⚠️ Store Impact model not loaded: {e}")
    STORE_LOADED = False

STORE_FEATURES = {
    "FFR12": {"label": "Fast-Food Restaurants Count", "default": 50, "desc": "Number of fast-food restaurants"},
    "FFRPTH12": {"label": "Fast-Food per 1000 Pop", "default": 0.5, "desc": "Fast-food restaurants per 1,000 inhabitants"},
    "SUPERC12": {"label": "Supermarkets Count", "default": 10, "desc": "Number of supermarkets"},
    "SUPERCPTH12": {"label": "Supermarkets per 1000 Pop", "default": 0.1, "desc": "Supermarkets per 1,000 inhabitants"},
    "FMRKT13": {"label": "Farmers Markets Count", "default": 3, "desc": "Number of farmers markets"},
    "FMRKTPTH13": {"label": "Farmers Markets per 1000", "default": 0.05, "desc": "Farmers markets per 1,000 inhabitants"},
    "PCT_FMRKT_SNAP13": {"label": "Markets Accepting SNAP (%)", "default": 30, "desc": "% of markets accepting SNAP"},
    "LACCESS_POP10": {"label": "Limited Access Population", "default": 5000, "desc": "People far from supermarket"},
    "LACCESS_LOWI10": {"label": "Low Income Limited Access", "default": 2000, "desc": "Low-income with limited access"},
    "LACCESS_HHNV10": {"label": "No Vehicle Limited Access", "default": 500, "desc": "Households without vehicle"},
    "food_access_score": {"label": "Food Access Score", "default": 6, "desc": "Composite access score"},
    "food_environment_index": {"label": "Food Environment Index", "default": 7, "desc": "Overall food environment"},
    "median_household_income": {"label": "Median Income ($)", "default": 50000, "desc": "Median household income"},
    "PERPOV10": {"label": "Poverty Rate (%)", "default": 15, "desc": "% below poverty line"},
    "food_insecurity_rate": {"label": "Food Insecurity Rate (%)", "default": 12, "desc": "% with food insecurity"},
    "SNAP_PART_RATE10": {"label": "SNAP Participation (%)", "default": 10, "desc": "SNAP participation rate"},
}


def predict_rf_view(request):
    """RF Health Score Prediction"""
    prediction = None
    prediction_context = None
    
    fields = []
    for f in RF_FEATURES:
        fields.append({
            'name': f,
            'label': RF_FEATURE_LABELS.get(f, f),
            'default': RF_DEFAULTS.get(f, 0)
        })
    
    if request.method == "POST" and RF_LOADED:
        input_map = {}
        for f in RF_FEATURES:
            raw_val = float(request.POST.get(f, 0))
            input_map[f] = raw_val
            # Update field value for display
            for field in fields:
                if field['name'] == f:
                    field['value'] = raw_val
        
        # Unit conversions
        if input_map['child_poverty_rate'] > 1.0:
            input_map['child_poverty_rate'] /= 100.0
        if input_map['physical_inactivity_rate'] > 1.0:
            input_map['physical_inactivity_rate'] /= 100.0
        if input_map['diabetes_prevalence_rate'] > 1.0:
            input_map['diabetes_prevalence_rate'] /= 100.0
        if input_map['food_access_score'] > 1.0:
            input_map['food_access_score'] /= 10.0
        if input_map['food_environment_index'] > 1.0:
            input_map['food_environment_index'] /= 10.0

        input_data = [input_map[f] for f in RF_FEATURES]
        X = np.array([input_data])
        X_scaled = rf_scaler.transform(X)
        pred = float(rf_model.predict(X_scaled)[0])
        prediction = round(pred, 3)
        
        # Determine risk level
        if pred < 0.3:
            prediction_context = {'level': 'Low Risk', 'color': 'success', 'message': 'Good health indicators for this area.'}
        elif pred < 0.6:
            prediction_context = {'level': 'Moderate Risk', 'color': 'warning', 'message': 'Some health concerns need monitoring.'}
        else:
            prediction_context = {'level': 'High Risk', 'color': 'danger', 'message': 'Significant health risks identified.'}
        
        print(f"🎯 RF Health Score: {prediction}")

    return render(request, "predictor/predict_rf.html", {
        "fields": fields,
        "prediction": prediction,
        "prediction_context": prediction_context
    })


def predict_store_impact_view(request):
    """Store Impact on Health Prediction (KNN)"""
    prediction = None
    prediction_context = None
    input_display = []
    
    fields = []
    for name, info in STORE_FEATURES.items():
        fields.append({
            'name': name,
            'label': info['label'],
            'default': info['default'],
            'desc': info['desc']
        })
    
    if request.method == "POST" and STORE_LOADED:
        input_data = []
        for name in STORE_FEATURES.keys():
            value = float(request.POST.get(name, 0))
            input_data.append(value)
            
            # Update field value for display
            for field in fields:
                if field['name'] == name:
                    field['value'] = value

            input_display.append({
                'label': STORE_FEATURES[name]['label'],
                'value': value
            })
        
        X = np.array([input_data])
        X_scaled = store_scaler.transform(X)
        pred = knn_model.predict(X_scaled)[0]
        pred_label = le.inverse_transform([pred])[0]
        
        prediction = pred_label
        
        # Determine color based on prediction
        pred_lower = str(pred_label).lower()
        if 'low' in pred_lower or 'good' in pred_lower or 'healthy' in pred_lower:
            prediction_context = {'color': 'success', 'message': 'Store environment supports healthy choices.'}
        elif 'moderate' in pred_lower or 'medium' in pred_lower:
            prediction_context = {'color': 'warning', 'message': 'Mixed impact from store environment.'}
        else:
            prediction_context = {'color': 'danger', 'message': 'Store environment may negatively impact health.'}
        
        print(f"🎯 Store Impact: {prediction}")

    return render(request, "predictor/predict_store.html", {
        "fields": fields,
        "prediction": prediction,
        "prediction_context": prediction_context,
        "input_display": input_display
    })
