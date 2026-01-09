# diabetes_risk/models.py - SVM Classifier for Diabetes Risk

import numpy as np
import os
import joblib
from django.conf import settings
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


class DiabetesRiskPredictor:
    """SVM-based Diabetes Risk Prediction Model"""
    
    FEATURES = [
        'adult_obesity_rate',           # 1
        'physical_inactivity_rate',     # 2
        'access_to_exercise_pct',       # 3
        'median_household_income',      # 4 (Duplicate?)
        'POVRATE10',                    # 5 (Poverty Rate)
        'food_insecurity_rate',         # 6
        'PCT_SNAP14',                   # 7 (SNAP Rate)
        'PCT_NSLP14',                   # 8 (School Lunch) - Default needed
        'FFRPTH12',                     # 9 (Fast Food) - Default needed
        'SUPERCPTH12',                  # 10 (Supercenters) - Default needed
        'LACCESS_LOWI10',               # 11 (Low Access) - Default needed
        'uninsured_rate',               # 12
        'primary_care_physicians_per_100k', # 13 - Default needed
        'PCT_65OLDER10',                # 14 (Seniors) - Default needed
        'MEDHHINC10',                   # 15 (Duplicate?)
        'SODA_PRICE10',                 # 16 - Default needed
        'MILK_PRICE10',                 # 17 - Default needed
        'RECFACPTH12'                   # 18 (Rec Facilities) - Default needed
    ]
    
    # Default feature means/medians for missing values (US Averages approx)
    # Default feature means/medians for missing values (US Averages approx)
    # NOTE: Decimal fields must be 0.0-1.0 to match model training data
    # Default feature means/medians for missing values (US Averages approx)
    # NOTE: Decimal fields must be 0.0-1.0 to match model training data
    FEATURE_DEFAULTS = {
        'adult_obesity_rate': 0.30,      # Mean ~0.37
        'physical_inactivity_rate': 0.25, # Mean ~0.30
        'access_to_exercise_pct': 0.65,   # Mean ~0.46
        'median_household_income': 50000, # Mean ~60k
        'POVRATE10': 15.0,                # Mean ~19.7
        'food_insecurity_rate': 0.12,     # Mean ~0.13
        'PCT_SNAP14': 12.0,               # Mean ~16.2
        'PCT_NSLP14': 10.15,              # Mean ~10.1 (CRITICAL FIX: Was 50)
        'FFRPTH12': 0.6,                  # Mean ~0.6
        'SUPERCPTH12': 0.01,              # Mean ~0.01
        'LACCESS_LOWI10': 16500.0,        # Mean ~16504 (Count, not %)
        'uninsured_rate': 0.12,           # Mean ~0.11
        'primary_care_physicians_per_100k': 41.5, # Mean ~41.5
        'PCT_65OLDER10': 14.5,            # Mean ~14.5
        'MEDHHINC10': 40838.0,            # Mean ~40838
        'SODA_PRICE10': 2.55,             # Mean ~2.55
        'MILK_PRICE10': 2.57,             # Mean ~2.57
        'RECFACPTH12': 0.04               # Mean ~0.04
    }
    
    # Map form fields to model fields
    FIELD_MAPPING = {
        'poverty_rate': 'POVRATE10',
        'snap_participation_rate': 'PCT_SNAP14',
        'median_household_income': ['median_household_income', 'MEDHHINC10'] # Maps to both
    }
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load the SVM model from trained .pkl files"""
        # Path to ml_models folder in this app
        app_dir = os.path.dirname(os.path.abspath(__file__))
        ml_models_dir = os.path.join(app_dir, 'ml_models')
        
        # Try to load trained model files
        model_path = os.path.join(ml_models_dir, 'diabetes_svm_model (1).pkl')
        scaler_path = os.path.join(ml_models_dir, 'diabetes_scaler (1).pkl')
        
        # Also check for files without (1) suffix
        if not os.path.exists(model_path):
            model_path = os.path.join(ml_models_dir, 'diabetes_svm_model.pkl')
        if not os.path.exists(scaler_path):
            scaler_path = os.path.join(ml_models_dir, 'diabetes_scaler.pkl')
        
        # Legacy path (in project root)
        legacy_path = os.path.join(settings.BASE_DIR, 'diabetes_svm_model.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                print(f"📦 Loading Diabetes SVM model from: {model_path}")
                print(f"📦 Loading Scaler from: {scaler_path}")
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                self.model_loaded = True
                print("✅ Diabetes SVM model and scaler loaded successfully!")
            except Exception as e:
                print(f"⚠️ Error loading model files: {e}")
                self.model_loaded = False
        elif os.path.exists(legacy_path):
            try:
                print(f"📦 Loading Diabetes SVM model from legacy path: {legacy_path}")
                model_data = joblib.load(legacy_path)
                self.model = model_data.get('model')
                self.scaler = model_data.get('scaler')
                self.model_loaded = True
                print("✅ Diabetes SVM model loaded from legacy file!")
            except Exception as e:
                print(f"⚠️ Error loading legacy model: {e}")
                self.model_loaded = False
        else:
            print("❌ No pre-trained model found. Please train the model using 'train_diabetes_model.py' first.")
            self.model_loaded = False
    
    def predict(self, input_data: dict) -> dict:
        """Make diabetes risk prediction"""
        print(f"\n🔍 DIABETES RISK PREDICTION - Input data:")
        for key, value in input_data.items():
            print(f"   • {key}: {value}")
        
        if not self.model_loaded:
            return {
                'error': True,
                'message': 'Model not available'
            }
        
        # Prepare input data including mapped fields
        prepared_data = input_data.copy()
        
        # Apply field mappings
        # Map 'poverty_rate' -> 'POVRATE10', etc.
        for form_field, model_field in self.FIELD_MAPPING.items():
            if form_field in prepared_data:
                val = prepared_data[form_field]
                if isinstance(model_field, list):
                    for mf in model_field:
                        prepared_data[mf] = val
                else:
                    prepared_data[model_field] = val
                    
        # UNIT CONVERSION:
        # Model expects decimals (0.0-1.0) for some rates, but form provides percentages (0-100)
        # Based on scaler means:
        # - Obesity (Mean ~0.37) -> Needs /100
        # - Inactivity (Mean ~0.30) -> Needs /100
        # - Exercise (Mean ~0.46) -> Needs /100
        # - Food Insecurity (Mean ~0.13) -> Needs /100
        # - Uninsured (Mean ~0.11) -> Needs /100
        # - Poverty (Mean ~19.7) -> Keep (Percentage)
        # - SNAP (Mean ~16.2) -> Keep (Percentage)
        
        decimal_fields = [
            'adult_obesity_rate', 
            'physical_inactivity_rate', 
            'access_to_exercise_pct', 
            'food_insecurity_rate', 
            'uninsured_rate'
        ]
        
        for field in decimal_fields:
            if field in prepared_data:
                try:
                    val = float(prepared_data[field])
                    # Only divide if input looks like a percentage (> 1.0)
                    # This handles if user enters 0.3 or 30
                    if val > 1.0: 
                        prepared_data[field] = val / 100.0
                except (ValueError, TypeError):
                    pass

        # Build feature vector in exact order
        feature_vector = []
        for feat in self.FEATURES:
            # Get value from prepared data or defaults
            value = prepared_data.get(feat, self.FEATURE_DEFAULTS.get(feat, 0))
            
            try:
                value = float(value)
            except (ValueError, TypeError):
                value = self.FEATURE_DEFAULTS.get(feat, 0)
            feature_vector.append(value)
            
        print(f"   • Feature vector length: {len(feature_vector)}")
        
        # Scale and predict
        X = np.array([feature_vector])
        X_scaled = self.scaler.transform(X)
        
        # Get probability
        probability = self.model.predict_proba(X_scaled)[0][1]
        prediction = self.model.predict(X_scaled)[0]
        
        print(f"🎯 Risk Probability: {probability:.2%}")
        
        return self._format_result(probability, feature_vector)
    
    def _format_result(self, probability: float, features: list) -> dict:
        """Format the prediction result"""
        # Determine risk category
        # CALIBRATED THRESHOLDS: Model outputs are compressed to 3-7% range
        # due to SVM Platt scaling. Thresholds adjusted accordingly:
        # - HIGH: >= 5.5% (top ~25% of model range)
        # - MEDIUM: 4.5% - 5.5% (middle range)
        # - LOW: < 4.5% (bottom ~40% of model range)
        if probability >= 0.055:
            category = "HIGH RISK"
            category_level = "high"
            color = "🔴"
            recommendation = "Immediate intervention recommended. Focus on obesity reduction and physical activity programs."
        elif probability >= 0.045:
            category = "MEDIUM RISK"
            category_level = "medium"
            color = "🟡"
            recommendation = "Preventive measures advised. Monitor diet and exercise habits."
        else:
            category = "LOW RISK"
            category_level = "low"
            color = "🟢"
            recommendation = "Continue healthy lifestyle. Regular check-ups recommended."
        
        # Identify top risk factors
        risk_factors = self._identify_risk_factors(features)
        
        return {
            'error': False,
            'success': True,
            'probability': round(probability * 100, 1),
            'prediction': int(probability >= 0.5),
            'category': f"{category} {color}",
            'category_level': category_level,
            'recommendation': recommendation,
            'risk_factors': risk_factors,
            'model_info': {
                'model_type': 'Support Vector Machine (SVM)',
                'kernel': 'RBF (Radial Basis Function)',
                'features': len(self.FEATURES)
            }
        }
    
    def _identify_risk_factors(self, features: list) -> list:
        """Identify the top contributing risk factors"""
        risk_factors = []
        
        # Check each feature against thresholds
        thresholds = {
            'adult_obesity_rate': (32, 'High obesity rate'),
            'physical_inactivity_rate': (28, 'High physical inactivity'),
            'food_environment_index': (5, 'Poor food environment'),  # Lower is worse
            'poverty_rate': (20, 'High poverty rate'),
            'food_insecurity_rate': (15, 'High food insecurity'),
            'access_to_exercise_pct': (50, 'Limited exercise access'),  # Lower is worse
            'uninsured_rate': (15, 'High uninsured rate'),
        }
        
        for i, (feat, (threshold, label)) in enumerate(thresholds.items()):
            if i < len(features):
                value = features[i] if i < len(features) else 0
                # For food_environment_index and access_to_exercise_pct, lower is worse
                if feat in ['food_environment_index', 'access_to_exercise_pct']:
                    if value < threshold:
                        risk_factors.append(label)
                else:
                    if value > threshold:
                        risk_factors.append(label)
        
        return risk_factors[:3]  # Return top 3 risk factors
