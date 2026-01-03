# diabetes_risk/forms.py
from django import forms


class DiabetesRiskForm(forms.Form):
    """Form for Diabetes Risk prediction using SVM"""
    
    adult_obesity_rate = forms.FloatField(
        label="Adult Obesity Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '30.0',
            'step': '0.1'
        }),
        help_text="Percentage of adults classified as obese (BMI ≥ 30)"
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
    
    food_environment_index = forms.FloatField(
        label="Food Environment Index (0-10)",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '7.5',
            'step': '0.1'
        }),
        help_text="Index of factors contributing to healthy food access (0=worst, 10=best)"
    )
    
    poverty_rate = forms.FloatField(
        label="Poverty Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '15.0',
            'step': '0.1'
        }),
        help_text="Percentage of population living below poverty line"
    )
    
    median_household_income = forms.FloatField(
        label="Median Household Income ($)",
        min_value=0,
        max_value=500000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '50000',
            'step': '1000'
        }),
        help_text="Average annual household income in the area"
    )
    
    food_insecurity_rate = forms.FloatField(
        label="Food Insecurity Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '12.0',
            'step': '0.1'
        }),
        help_text="Percentage of population with limited access to adequate food"
    )
    
    snap_participation_rate = forms.FloatField(
        label="SNAP Participation Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '10.0',
            'step': '0.1'
        }),
        help_text="Percentage of population receiving SNAP benefits"
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
        help_text="Percentage of population with access to exercise facilities"
    )
    
    uninsured_rate = forms.FloatField(
        label="Uninsured Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '12.0',
            'step': '0.1'
        }),
        help_text="Percentage of population without health insurance"
    )
