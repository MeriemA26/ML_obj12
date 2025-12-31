import joblib
import numpy as np

model = joblib.load("prediction/models_ml/knn.pkl")
scaler = joblib.load("prediction/models_ml/scaler.pkl")

# Exemple features (19 colonnes, ordre = model_features)
example_features = np.array([[
    50000, 10, 30, 20, 1.5, 2.0, 0, 5, 8, 12, 60, 15, 25, 30, 18, 0.08, 120, 10, 5
]])
features_scaled = scaler.transform(example_features)
prediction = model.predict(features_scaled)
print("Prédiction :", prediction[0])