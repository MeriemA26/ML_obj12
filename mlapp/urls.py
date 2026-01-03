from django.urls import path
from . import views

app_name = 'mlapp'

urlpatterns = [
    path('', views.predict_view, name='predict'),
    path('api/test/', views.test_prediction, name='test'),
]
