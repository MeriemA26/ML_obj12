# obj1/models.py - MODÈLE POUR L'OBJECTIF 1 avec uniquement prédiction ML

import joblib
import pandas as pd
import numpy as np
import os
from django.conf import settings

class FoodQualityPredictor:
    """Classe pour utiliser le modèle Random Forest optimisé pour la qualité alimentaire"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = []
        self.feature_means = {}
        self.load_model()
    
    def load_model(self):
        """Charger le modèle Random Forest optimisé pour la qualité alimentaire"""
        try:
            model_path = os.path.join(settings.BASE_DIR, 'food_quality_model_final.pkl')
            print(f"📦 Recherche du modèle à: {model_path}")
            print(f"   • Fichier existe: {os.path.exists(model_path)}")
            
            if not os.path.exists(model_path):
                model_path = os.path.join(settings.BASE_DIR, '..', 'food_quality_model_final.pkl')
                print(f"📦 Essai chemin alternatif: {model_path}")
                print(f"   • Fichier existe: {os.path.exists(model_path)}")
            
            if not os.path.exists(model_path):
                print(f"❌ Modèle non trouvé")
           
            
            print(f"🔄 Chargement du modèle...")
            
            import __main__
            
            def predire_qualite_finale(valeurs_dict, model, scaler, features, feature_means):
                input_vector = []
                for feat in features:
                    if feat in valeurs_dict:
                        value = valeurs_dict[feat]
                        if isinstance(value, str):
                            value = float(value.replace(',', '.'))
                        else:
                            value = float(value)
                        input_vector.append(value)
                    else:
                        input_vector.append(feature_means.get(feat, 0))
                
                input_scaled = scaler.transform(pd.DataFrame([input_vector], columns=features))
                score = model.predict(input_scaled)[0]
                return score
            
            __main__.predire_qualite_finale = predire_qualite_finale
            
            with open(model_path, 'rb') as f:
                model_data = joblib.load(f)
            
            print(f"✅ Modèle chargé avec succès!")
            
            self.model = model_data.get('model')
            self.scaler = model_data.get('scaler')
            self.features = model_data.get('features', [])
            self.feature_means = model_data.get('feature_means', {})
            
            if not self.features:
                self.features = [
                    'median_household_income', 
                    'physical_inactivity_rate', 
                    'food_insecurity_rate',
                    'access_to_exercise_pct', 
                    'MEDHHINC10', 
                    'FMRKTPTH13',
                    'dentists_per_100k', 
                    'PCH_RECFACPTH_07_12'
                ]
            
            if not self.feature_means:
                self.feature_means = {
                    'median_household_income': 50000,
                    'physical_inactivity_rate': 25.0,
                    'food_insecurity_rate': 0.12,
                    'access_to_exercise_pct': 65.0,
                    'MEDHHINC10': 50000,
                    'FMRKTPTH13': 1.2,
                    'dentists_per_100k': 75.0,
                    'PCH_RECFACPTH_07_12': 3.5
                }
            
            print(f"🎯 Random Forest (Qualité) initialisé")
            print(f"   • {len(self.features)} features")
            print(f"   • Modèle: {'✓' if self.model else '✗'}")
            print(f"   • Scaler: {'✓' if self.scaler else '✗'}")
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            import traceback
            traceback.print_exc()
            
    

    
    def predict(self, input_data):
        """Prédiction du score de qualité alimentaire uniquement avec le modèle ML"""
        print(f"\n🔍 PRÉDICTION - Données reçues:")
        for key, value in input_data.items():
            print(f"   • {key}: {value}")
        
        normalized_data = {}
        field_mapping = {
            'median_household_income': ['median_household_income', 'revenu'],
            'physical_inactivity_rate': ['physical_inactivity_rate', 'inactivite'],
            'food_insecurity_rate': ['food_insecurity_rate', 'insecurite'],
            'access_to_exercise_pct': ['access_to_exercise_pct', 'acces_sport'],
            'MEDHHINC10': ['MEDHHINC10', 'revenu_2010'],
            'FMRKTPTH13': ['FMRKTPTH13', 'marches'],
            'dentists_per_100k': ['dentists_per_100k', 'dentistes'],
            'PCH_RECFACPTH_07_12': ['PCH_RECFACPTH_07_12', 'evolution_installations']
        }
        
        for expected_name, possible_names in field_mapping.items():
            found = None
            for name in possible_names:
                if name in input_data:
                    found = input_data[name]
                    break
            if found is None:
                found = self.feature_means.get(expected_name, 0)
            try:
                found = float(found.replace(',', '.')) if isinstance(found, str) else float(found)
            except:
                found = float(self.feature_means.get(expected_name, 0))
            normalized_data[expected_name] = found
        
        score = self._predict_with_model(normalized_data)
        return self._format_result(score)
    
    def _predict_with_model(self, data):
        """Prédiction avec le modèle ML uniquement"""
        input_vector = [data.get(feat, self.feature_means.get(feat, 0)) for feat in self.features]
        input_df = pd.DataFrame([input_vector], columns=self.features)
        input_scaled = self.scaler.transform(input_df)
        score = self.model.predict(input_scaled)[0]
        print(f"🎯 Score ML: {score:.1f}")
        return score
    
    def _format_result(self, score):
        """Formater le résultat final"""
        if score < 30:
            categorie = "LOW"
            couleur = "🔴"
            recommandation = "URGENT INTERVENTION NEEDED"
            niveau = "Low"
        elif score < 45:
            categorie = "MEDIUM"
            couleur = "🟡"
            recommandation = "POSSIBLE IMPROVEMENTS"
            niveau = "Medium"
        else:
            categorie = "HIGH"
            couleur = "🔵"
            recommandation = "EXCELLENT QUALITY"
            niveau = "High"
        
        return {
            'error': False,
            'success': True,
            'score': round(score, 1),
            'category': f"{categorie} {couleur}",
            'category_level': niveau,
            'recommendation': recommandation,
            'model_info': {
                'model_type': 'Random Forest (Régression)',
                'performance': 'R² = 0.9985',
                'features': len(self.features)
            }
        }
