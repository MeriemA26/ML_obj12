# obj1/urls.py
from django.urls import path
from . import views

app_name = 'food_quality'

urlpatterns = [
    path('', views.QualityHomeView.as_view(), name='quality_home'),
    path('predict/', views.QualityPredictView.as_view(), name='quality_predict'),
    path('api/', views.QualityAPIView.as_view(), name='quality_api'),
]