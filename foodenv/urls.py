from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predictor/', include('predictor.urls')),  # inclut toutes les URLs de predictor
    path('', lambda request: redirect('predictor/', permanent=False)),  # racine redirige vers predictor
    path('segment/', include('segment.urls')),  # <-- ajouter cette ligne

]
