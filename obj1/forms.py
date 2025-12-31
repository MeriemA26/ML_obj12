# obj1/forms.py
from django import forms

class FoodQualityForm(forms.Form):
    """Formulaire pour la qualité alimentaire"""
    
    median_household_income = forms.FloatField(
        label="Median Household Income ($)",
        min_value=0,
        max_value=500000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '50000',
            'step': '1000'
        }),
        help_text="Average annual income of households in the area"
    )
    
    physical_inactivity_rate = forms.FloatField(
        label="Physical Inactivity Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '25.0',
            'step': '0.1'
        }),
        help_text="Percentage of adults who are physically inactive"
    )
    
    food_insecurity_rate = forms.FloatField(
        label="Food Insecurity Rate (%)",
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.12',
            'step': '0.01'
        }),
        help_text="Percentage of population with limited access to food"
    )
    
    access_to_exercise_pct = forms.FloatField(
        label="Access to Exercise Facilities (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '65.0',
            'step': '0.1'
        }),
        help_text="Percent of population with access to sports/recreation facilities"
    )
    
    MEDHHINC10 = forms.FloatField(
        label="Median Household Income 2010 ($)",
        min_value=0,
        max_value=500000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '50000',
            'step': '1000'
        }),
        help_text="Historical median household income"
    )
    
    FMRKTPTH13 = forms.FloatField(
        label="Farmers Markets per 1000 People",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1.2',
            'step': '0.1'
        }),
        help_text="Number of local farmers markets per 1000 inhabitants"
    )
    
    dentists_per_100k = forms.FloatField(
        label="Dentists per 100,000 People",
        min_value=0,
        max_value=500,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '75.0',
            'step': '1'
        }),
        help_text="Number of dentists available per 100,000 inhabitants"
    )
    
    PCH_RECFACPTH_07_12 = forms.FloatField(
        label="Recreational Facilities Change 2007–2012 (%)",
        min_value=-100,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '3.5',
            'step': '0.1'
        }),
        help_text="Percentage change in recreational facilities over 2007–2012"
    )