# diabetes_risk/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
import json
from .forms import DiabetesRiskForm
from .models import DiabetesRiskPredictor

# Initialize the predictor ONCE
try:
    DIABETES_PREDICTOR = DiabetesRiskPredictor()
    print(f"✅ Diabetes Risk Predictor initialized")
except Exception as e:
    print(f"⚠️ Error initializing Diabetes Predictor: {str(e)}")
    DIABETES_PREDICTOR = None


class DiabetesRiskHomeView(TemplateView):
    """Home page for Diabetes Risk prediction"""
    template_name = 'diabetes_risk/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DiabetesRiskForm()
        context['model_type'] = "Support Vector Machine (SVM)"
        context['model_kernel'] = "RBF Kernel"
        return context


class DiabetesRiskPredictView(View):
    """View to handle predictions"""
    
    def get(self, request):
        return redirect('diabetes_risk:home')
    
    def post(self, request):
        form = DiabetesRiskForm(request.POST)
        
        if form.is_valid():
            input_data = form.cleaned_data
            
            if DIABETES_PREDICTOR is None:
                return render(request, 'diabetes_risk/index.html', {
                    'form': form,
                    'error': 'Model not available',
                    'model_type': "Support Vector Machine (SVM)",
                    'model_kernel': "RBF Kernel"
                })
            
            # Make prediction
            result = DIABETES_PREDICTOR.predict(input_data)
            
            context = {
                'form': form,
                'result': result,
                'model_type': "Support Vector Machine (SVM)",
                'model_kernel': "RBF Kernel"
            }
            
            return render(request, 'diabetes_risk/index.html', context)
        
        # Invalid form
        return render(request, 'diabetes_risk/index.html', {
            'form': form,
            'model_type': "Support Vector Machine (SVM)",
            'model_kernel': "RBF Kernel"
        })


class DiabetesRiskAPIView(View):
    """API endpoint for predictions (JSON)"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if DIABETES_PREDICTOR is None:
                return JsonResponse({
                    'error': True,
                    'message': 'Model not available'
                })
            
            result = DIABETES_PREDICTOR.predict(data)
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error: {str(e)}'
            })
