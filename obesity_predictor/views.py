import os
import json
import joblib
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse

# Base directory of this app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, "ml")

# Load ML artifacts ONCE
model = joblib.load(os.path.join(ML_DIR, "obesity_xgboost_model.pkl"))
scaler = joblib.load(os.path.join(ML_DIR, "scaler.pkl"))
label_encoder = joblib.load(os.path.join(ML_DIR, "label_encoder.pkl"))

with open(os.path.join(ML_DIR, "model_info.json")) as f:
    model_info = json.load(f)

FEATURES = model_info["features"]

# Descriptions des features pour le template
feature_config = {
    'MEDHHINC10': {"label": "Median Household Income", "desc": "Revenu médian des ménages ($)", "example": 50000},
    'POVRATE10': {"label": "Poverty Rate", "desc": "Pourcentage de la population sous le seuil de pauvreté (%)", "example": 15.5},
    'Unemployment_Rate_county': {"label": "Unemployment Rate", "desc": "Taux de chômage dans le comté (%)", "example": 5.2},
    'physical_inactivity_rate': {"label": "Physical Inactivity", "desc": "Pourcentage d'adultes inactifs (%)", "example": 24.5},
    'diabetes_prevalence_rate': {"label": "Diabetes Prevalence", "desc": "Taux de diabète dans la population (%)", "example": 10.8},
    'food_insecurity_rate': {"label": "Food Insecurity", "desc": "Accès limité à une alimentation suffisante (%)", "example": 12.3},
    'food_environment_index': {"label": "Food Environment Index", "desc": "Indice de 0 (mauvais) à 10 (bon)", "example": 7.5},
    'PCT_65OLDER10': {"label": "Seniors (>65y)", "desc": "Pourcentage de personnes âgées de 65+ ans (%)", "example": 18.2},
    'PCT_18YOUNGER10': {"label": "Youth (<18y)", "desc": "Pourcentage de moins de 18 ans (%)", "example": 22.4},
    'LACCESS_POP10': {"label": "Low Access Population", "desc": "Population avec accès difficile aux magasins (nombre)", "example": 5000}
}


def predict_obesity(request):
    prediction_label = None

    # Prepare features for the template
    features_for_template = []
    for feature in FEATURES:
        conf = feature_config.get(feature, {})
        features_for_template.append({
            "name": feature,
            "label": conf.get("label", feature),
            "description": conf.get("desc", ""),
            "example": conf.get("example", ""),
        })

    if request.method == "POST":
        input_data = []
        for feature in FEATURES:
            value = float(request.POST.get(feature))
            input_data.append(value)

        X = np.array([input_data])
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)[0]
        prediction_label = label_encoder.inverse_transform([prediction])[0]

    return render(
        request,
        "obesity_predictor/predict.html",
        {
            "features": features_for_template,
            "prediction": prediction_label
        }
    )




def analytics_framework(request):
    return render(request, "obesity_predictor/analytics.html")
