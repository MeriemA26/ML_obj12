# diabetes_risk/urls.py
from django.urls import path
from .views import DiabetesRiskHomeView, DiabetesRiskPredictView, DiabetesRiskAPIView

app_name = 'diabetes_risk'

urlpatterns = [
    path('', DiabetesRiskHomeView.as_view(), name='home'),
    path('predict/', DiabetesRiskPredictView.as_view(), name='predict'),
    path('api/predict/', DiabetesRiskAPIView.as_view(), name='api_predict'),
]
