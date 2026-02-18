from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('predict1/', views.PredictView.as_view(), name='predict'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
   
]