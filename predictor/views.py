# predictor/views.py
from django.shortcuts import render
import numpy as np
import joblib

# Charger le modèle et les objets ML une seule fois
knn = joblib.load('predictor/ml/Store Impact on Health.pkl')
le = joblib.load('predictor/ml/label_encoder_health.pkl')
scaler = joblib.load('predictor/ml/scaler_features_health.pkl')
scaler_health = joblib.load('predictor/ml/scaler_health_score.pkl')

# Liste de toutes les features utilisées dans le modèle
FEATURES = {
    # Store types
    "FFR12": "Number of fast-food restaurants in the county. Higher values often indicate greater exposure to unhealthy food.",
    "FFRPTH12": "Fast-food restaurants per 1,000 inhabitants. Measures fast-food density relative to population.",
    "SUPERC12": "Number of supermarkets providing access to fresh and healthy food options.",
    "SUPERCPTH12": "Supermarkets per 1,000 inhabitants. Higher values indicate better access to healthy food.",
    "FMRKT13": "Number of farmers’ markets offering fresh and local food.",
    "FMRKTPTH13": "Farmers’ markets per 1,000 inhabitants. Indicates availability of fresh food.",
    "PCT_FMRKT_SNAP13": "Percentage of farmers’ markets that accept SNAP benefits, improving access for low-income populations.",

    # Food access
    "LACCESS_POP10": "Number of people living far from a supermarket, indicating food access limitations.",
    "LACCESS_LOWI10": "Low-income population with limited access to healthy food.",
    "LACCESS_HHNV10": "Households without a vehicle and with limited access to supermarkets.",
    "food_access_score": "Composite score measuring overall access to healthy food. Higher values indicate better access.",
    "food_environment_index": "Overall index representing food availability, affordability, and quality.",

    # Socio-economic
    "median_household_income": "Median household income in the county, reflecting economic purchasing power.",
    "PERPOV10": "Percentage of the population living below the poverty line.",
    "food_insecurity_rate": "Percentage of people uncertain about having enough food.",
    "SNAP_PART_RATE10": "Rate of participation in the SNAP food assistance program.",
  
}

# Exemple d'information sur les ranges des features (peut être ajusté)
model_info = {
    "feature_ranges": {feature: (0, 1) for feature in FEATURES}  # placeholder, tu peux mettre les vraies valeurs
}

def predict_view(request):
    prediction_label = None

    features_data = []

    for feature, description in FEATURES.items():
        features_data.append({
            "name": feature,
            "description": description,
            "default": 0  # or any default value you want
        })

    if request.method == "POST":
        input_data = []

        for feature in FEATURES:
            value = float(request.POST.get(feature, 0))
            input_data.append(value)

        X = np.array([input_data])
        X_scaled = scaler.transform(X)

        prediction = knn.predict(X_scaled)[0]
        prediction_raw = le.inverse_transform([prediction])[0]

        # Wrap prediction in a full phrase
        prediction_label = f"The Health Risk is {prediction_raw}"

    return render(
        request,
        "predictor/predict.html",
        {
            "features_data": features_data,
            "prediction": prediction_label
        }
    )

def analytics_framework_view(request):
    return render(request, 'analytics_framework.html')
