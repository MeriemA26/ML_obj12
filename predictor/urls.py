from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path("", views.predict_rf_view, name="predict_rf"),  # RF Health Score
    path("store/", views.predict_store_impact_view, name="predict_store"),  # Store Impact on Health
]
