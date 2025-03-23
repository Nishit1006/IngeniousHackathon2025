from django import forms
from .models import Farmland

class FarmlandRegistrationForm(forms.ModelForm):
    """Form for registering farmland details."""
    
    SOIL_TYPE_CHOICES = [
        ('black', 'Black Soil'),
        ('alluvial', 'Alluvial Soil'),
        ('red', 'Red Soil'),
        ('laterite', 'Laterite Soil'),
        ('sandy', 'Sandy Soil'),
        ('clay', 'Clay Soil'),
        ('loam', 'Loam Soil'),
    ]
    
    IRRIGATION_CHOICES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler System'),
        ('canal', 'Canal Irrigation'),
        ('well', 'Well Water'),
        ('rain', 'Rain-fed'),
    ]
    
    soil_type = forms.ChoiceField(choices=SOIL_TYPE_CHOICES)
    irrigation_source = forms.MultipleChoiceField(
        choices=IRRIGATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select all applicable irrigation methods"
    )
    
    class Meta:
        model = Farmland
        fields = ['name', 'area', 'latitude', 'longitude', 'address', 'soil_type', 'irrigation_source']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_irrigation_source(self):
        """Convert list of irrigation sources to comma-separated string."""
        irrigation_sources = self.cleaned_data.get('irrigation_source', [])
        return ', '.join(irrigation_sources) 