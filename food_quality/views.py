# obj1/views.py - VUES POUR L'OBJECTIF 1
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
import json
from .forms import FoodQualityForm
from .models import FoodQualityPredictor

# Instancier le prédicteur UNE SEULE FOIS
try:
    PREDICTOR = FoodQualityPredictor()
    print(f"✅ Prédicteur Qualité Alimentaire initialisé")
except Exception as e:
    print(f"⚠️ Erreur initialisation: {str(e)}")
    PREDICTOR = None

class QualityHomeView(TemplateView):
    """Page d'accueil pour la qualité alimentaire"""
    template_name = 'quality/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FoodQualityForm()
        context['model_score'] = "9.9/10 ⭐"
        context['model_type'] = "Random Forest Régression"
        context['model_performance'] = "R² = 0.9985"
        return context

class QualityPredictView(View):
    """Vue pour traiter les prédictions"""
    
    def get(self, request):
        return redirect('quality_home')
    
    def post(self, request):
        form = FoodQualityForm(request.POST)
        
        if form.is_valid():
            input_data = form.cleaned_data
            
            if PREDICTOR is None:
                return render(request, 'quality/index.html', {
                    'form': form,
                    'error': 'Model not available',
                    'model_score': "9.9/10 ⭐",
                    'model_type': "Random Forest Régression"
                })
            
            # Prédiction
            result = PREDICTOR.predict(input_data)
            
            context = {
                'form': form,
                'result': result,
                'model_score': "9.9/10 ⭐",
                'model_type': "Random Forest Régression",
                'model_performance': "R² = 0.9985"
            }
            
            return render(request, 'quality/index.html', context)
        
        # Formulaire invalide
        return render(request, 'quality/index.html', {
            'form': form,
            'model_score': "9.9/10 ⭐",
            'model_type': "Random Forest Régression"
        })

class QualityAPIView(View):
    """API pour les prédictions (JSON)"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if PREDICTOR is None:
                return JsonResponse({
                    'error': True,
                    'message': 'Model not available'
                })
            
            result = PREDICTOR.predict(data)
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error: {str(e)}'
            })