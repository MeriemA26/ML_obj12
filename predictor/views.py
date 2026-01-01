import os
import joblib
import numpy as np
from django.shortcuts import render

# Chemin vers le dossier ml
ML_DIR = os.path.join(os.path.dirname(__file__), "ml")

# Charger le scaler et le modèle
rf_scaler = joblib.load(os.path.join(ML_DIR, "rf_scaler.pkl"))
rf_model = joblib.load(os.path.join(ML_DIR, "rf_model.pkl"))

# Features utilisées
RF_FEATURES = [
    'median_household_income', 'child_poverty_rate', 'physical_inactivity_rate',
    'food_access_score', 'POVRATE10', 'PCT_SNAP14', 'diabetes_prevalence_rate',
    'food_environment_index'
]
def predict_rf_view(request):
    prediction = None
    if request.method == "POST":
        # Récupérer les valeurs du formulaire
        input_data = [float(request.POST.get(f, 0)) for f in RF_FEATURES]
        X = np.array([input_data])

        # Appliquer le scaler
        X_scaled = rf_scaler.transform(X)

        # Prédiction avec Random Forest
        pred = float(rf_model.predict(X_scaled)[0])

        # Arrondir pour affichage
        prediction = round(pred, 3)  # par exemple 0.287

    return render(request, "predictor/predict_rf.html",
                  {"features": RF_FEATURES, "prediction": prediction})
