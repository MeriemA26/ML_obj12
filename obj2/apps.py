from django.apps import AppConfig


class Obj2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obj2'

    def ready(self):
        # Charger le modèle au démarrage
        try:
            from .models import FoodDesertPredictor
            predictor = FoodDesertPredictor()
            print("✅ Modèle ML chargé avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du modèle: {e}")