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
feature_descriptions = {
    'MEDHHINC10': "Revenu médian des ménages, influence l'accès à la nourriture et au sport.",
    'POVRATE10': "Pourcentage de la population sous le seuil de pauvreté.",
    'Unemployment_Rate_county': "Taux de chômage dans le comté.",
    'physical_inactivity_rate': "Pourcentage d'adultes ne pratiquant pas d'activité physique.",
    'diabetes_prevalence_rate': "Pourcentage de la population ayant le diabète.",
    'food_insecurity_rate': "Proportion de la population avec un accès limité à une alimentation suffisante.",
    'food_environment_index': "Indice reflétant la disponibilité d'aliments sains.",
    'PCT_65OLDER10': "Pourcentage de personnes âgées de 65 ans et plus.",
    'PCT_18YOUNGER10': "Pourcentage de personnes âgées de moins de 18 ans.",
    'LACCESS_POP10': "Population ayant un accès limité aux supermarchés."
}


def test_prediction(request):
    """
    Test endpoint to verify ML prediction pipeline
    """
    input_data = [model_info["feature_ranges"][f]["default"] for f in FEATURES]

    # Convert to numpy array
    X = np.array([input_data])

    # Scale
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0]
    prediction_label = label_encoder.inverse_transform([prediction])[0]

    return JsonResponse({
        "prediction_class": prediction_label
    })


def predict_obesity(request):
    prediction_label = None

    # Prepare features for the template
    features_for_template = []
    for feature in FEATURES:
        features_for_template.append({
            "name": feature,
            "description": feature_descriptions.get(feature, ""),
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
        "predictor/predict.html",
        {
            "features": features_for_template,
            "prediction": prediction_label
        }
    )




def analytics_framework(request):
    return render(request, "predictor/analytics.html")
