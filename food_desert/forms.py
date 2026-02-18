from django import forms

class FoodDesertForm(forms.Form):
    """Formulaire adapté au modèle SVM (8 features)"""
    
    # 1. ÉCONOMIQUE
    median_household_income = forms.FloatField(
        label="Median Household Income ($)",
        min_value=0,
        max_value=500000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50000',
            'step': '1000'
        })
    )
    
    # 2. SOCIAL
    POVRATE10 = forms.FloatField(
        label="Poverty Rate (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 15.5',
            'step': '0.1'
        })
    )
    
    # 3. DÉMOGRAPHIQUE
    PCT_65OLDER10 = forms.FloatField(
        label="Population 65+ (%)",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 14.8',
            'step': '0.1'
        })
    )
    
    # 4. GÉOGRAPHIQUE - ACCÈS LIMITÉ (SANS VÉHICULE)
    LACCESS_HHNV10 = forms.FloatField(
        label="Households without vehicle within 1km of a supermarket",
        min_value=0,
        max_value=10000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 150',
            'step': '1'
        })
    )
    
    # 5. INFRASTRUCTURE ALIMENTAIRE
    GROC12 = forms.FloatField(
        label="Number of Grocery Stores",
        min_value=0,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50',
            'step': '1'
        })
    )
    
    # 6. SANTÉ
    adult_obesity_rate = forms.FloatField(
        label="Adult Obesity Rate (proportion)",
        min_value=0.1,
        max_value=0.7,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 0.30 (30%)',
            'step': '0.01'
        })
    )
    
    # 7. INFRASTRUCTURE RÉCRÉATIVE
    RECFACPTH12 = forms.FloatField(
        label="Recreational Facilities per 1000 inhabitants",
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 0.25',
            'step': '0.01'
        })
    )
    
    # 8. ACCÈS GÉNÉRAL LIMITÉ
    LACCESS_POP10 = forms.FloatField(
        label="Population with limited access within 1km of a supermarket",
        min_value=0,
        max_value=50000,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1200',
            'step': '10'
        })
    )
    
    def clean(self):
        """Validation supplémentaire"""
        cleaned_data = super().clean()
        
        # Validation des pourcentages
        percent_fields = ['POVRATE10', 'PCT_65OLDER10']
        
        for field in percent_fields:
            value = cleaned_data.get(field)
            if value is not None and (value < 0 or value > 100):
                self.add_error(field, 'Doit être entre 0 et 100%')
        
        return cleaned_data