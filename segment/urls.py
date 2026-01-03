from django.urls import path
from . import views

urlpatterns = [
    path('', views.segment_home, name='segment_home'),
    path('predict/', views.predict_segment, name='predict_segment'),
]
