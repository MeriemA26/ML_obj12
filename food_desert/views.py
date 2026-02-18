# views.py - VERSION FINALE CORRIGÉE
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
import json
from .forms import FoodDesertForm
from .models import FoodDesertPredictor

# Instancier le prédicteur UNE SEULE FOIS
try:
    PREDICTOR = FoodDesertPredictor()
    print(f"✅ Prédicteur Random Forest initialisé")
except Exception as e:
    print(f"⚠️ Erreur initialisation prédicteur: {str(e)}")
    PREDICTOR = None

class HomeView(TemplateView):
    """Page d'accueil avec formulaire"""
    template_name = 'predictor/food_desert.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FoodDesertForm()
        context['model_score'] = "9.5/10 ⭐"
        context['model_type'] = "Optimized Random Forest"  # NOUVEAU
        context['model_auc'] = "0.920"  # NOUVEAU
        context['model_recall'] = "85.0%"  # NOUVEAU
        return context

class PredictView(View):
    """Vue pour traiter les prédictions"""
    
    def get(self, request):
        return redirect('home')
    
    def post(self, request):
        form = FoodDesertForm(request.POST)
        
        if form.is_valid():
            input_data = form.cleaned_data
            
            if PREDICTOR is None:
                return render(request, 'predictor/food_desert.html', {
                    'form': form,
                    'error': 'Model not available',
                    'model_score': "9.5/10 ⭐",
                    'model_type': "Optimized Random Forest"  # NOUVEAU
                })
            
            # Prédiction
            result = PREDICTOR.predict(input_data)
            
            context = {
                'form': form,
                'result': result,
                'model_score': "9.5/10 ⭐",
                'model_type': "Optimized Random Forest",  # NOUVEAU
                'model_auc': "0.920",  # NOUVEAU
                'model_recall': "85.0%"  # NOUVEAU
            }
            
            return render(request, 'predictor/food_desert.html', context)
        
        # Formulaire invalide
        return render(request, 'predictor/food_desert.html', {
            'form': form,
            'model_score': "9.5/10 ⭐",
            'model_type': "Optimized Random Forest"  # NOUVEAU
        })

# ... PredictAPIView reste inchangé ...
class DashboardView(TemplateView):
    """Vue pour le tableau de bord Power BI"""
    template_name = 'dashboard.html'

class PredictAPIView(View):
    """API pour les prédictions (format JSON)"""
    
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