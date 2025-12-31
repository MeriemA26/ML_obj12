import joblib
import os

BASE_DIR = 'C:\\Users\\merya\\Desktop\\3AI\\sem1\\pyhton\\machineL\\ml_project'
model_path = os.path.join(BASE_DIR, 'food_quality_model_final.pkl')

print(f"Testing model at: {model_path}")
print(f"File exists: {os.path.exists(model_path)}")

if os.path.exists(model_path):
    try:
        model_data = joblib.load(model_path)
        print(f"✅ Model loaded successfully!")
        print(f"   Keys: {list(model_data.keys())}")
        print(f"   Features: {model_data.get('features', 'Not found')}")
    except Exception as e:
        print(f"❌ Error loading: {e}")
        import traceback
        traceback.print_exc()