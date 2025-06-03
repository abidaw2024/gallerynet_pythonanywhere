# apps/gallery/forms.py

from django import forms
from .models import ObraDeArte

class ObraForm(forms.ModelForm):
    class Meta:
        model = ObraDeArte
        fields = '__all__'
