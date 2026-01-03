import os
import joblib
import numpy as np
from django.shortcuts import render

# =============================
# Paths
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, 'segment', 'ml', 'svm_segment_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'segment', 'ml', 'scaler_segment.pkl')

# Charger modèle et scaler
svm_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# =============================
# Features exactes utilisées lors de l'entraînement
# =============================
FEATURES = [
    'MEDHHINC10',
    'Unemployment_Rate_county',
    'Labor_Force',
    'Employed',
    'Unemployed',
    'median_household_income'  # attention au nom exact !
]

# =============================
# Page principale
# =============================
def segment_home(request):
    return render(request, 'segment/predict_segment.html', {
        'features': FEATURES
    })

# =============================
# Prediction
# =============================
def predict_segment(request):
    prediction = None
    if request.method == 'POST':
        # Récupérer les valeurs envoyées par le formulaire
        values = []
        for feature in FEATURES:
            value = float(request.POST.get(feature, 0))
            values.append(value)

        # Convertir en array numpy et scaler
        X = np.array(values).reshape(1, -1)
        X_scaled = scaler.transform(X)

        # Prédiction
        prediction = svm_model.predict(X_scaled)[0]

    return render(request, 'segment/predict_segment.html', {
        'features': FEATURES,
        'prediction': int(prediction) if prediction is not None else None
    })
