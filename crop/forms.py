from django import forms
from .models import CropListing

class CropListingForm(forms.ModelForm):
    class Meta:
        model = CropListing
        fields = ['crop_name', 'quantity', 'unit', 'price_per_unit', 'description', 'location', 'contact_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Enter your contact number'}),
        } 