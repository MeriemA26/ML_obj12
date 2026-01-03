from django.urls import path
from .views import predict_view, test_prediction

urlpatterns = [
    path('', predict_view, name='predict'),
    path('test/', test_prediction, name='test'),
]
