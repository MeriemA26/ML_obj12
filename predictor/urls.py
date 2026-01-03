from django.urls import path
from . import views

urlpatterns = [
    path("", views.predict_rf_view, name="predict_rf_root"),  # racine du predictor/
    path("predict_rf/", views.predict_rf_view, name="predict_rf"),
]
