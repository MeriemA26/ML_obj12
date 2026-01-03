import os
import json
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, 'ml')

model = joblib.load(os.path.join(ML_DIR, 'run_1_best_model_KNN.pkl'))
scaler = joblib.load(os.path.join(ML_DIR, 'run_1_scaler.pkl'))

with open(os.path.join(ML_DIR, 'run_1_model_info.json')) as f:
    model_info = json.load(f)

FEATURES = model_info['feature_names']


def test_prediction(request):
    # Use default values from feature_ranges if available, otherwise use zeros
    values = []
    for f in FEATURES:
        if 'feature_ranges' in model_info and f in model_info['feature_ranges']:
            values.append(model_info['feature_ranges'][f].get('default', 0))
        else:
            values.append(0)

    X = pd.DataFrame([values], columns=FEATURES).values
    pred = model.predict(X)[0]

    return JsonResponse({'prediction': float(pred)})


def predict_view(request):
    prediction = None
    input_values = {}

    if request.method == 'POST':
        values = []
        for f in FEATURES:
            val = float(request.POST.get(f))
            values.append(val)
            input_values[f] = val

        X = pd.DataFrame([values], columns=FEATURES).values
        pred = model.predict(X)[0]
        prediction = f"{float(pred):,.2f}"


    # Create feature ranges from model_info if available
    feature_ranges = {}
    if 'feature_ranges' in model_info:
        feature_ranges = model_info['feature_ranges']
    else:
        # Default ranges if not provided
        for f in FEATURES:
            feature_ranges[f] = {'default': 0, 'min': 0, 'max': 100}

    return render(
        request,
        'predict.html',
        {
            'features': FEATURES,
            'feature_ranges': feature_ranges,
            'prediction': prediction,
            'input_values': input_values
        }
    )
