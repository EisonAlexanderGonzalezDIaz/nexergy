from django import forms
from .models import Entidad

class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ['nombre', 'municipio', 'tipo', 'nit']
        widgets = {
            'nombre':    forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-select'}),
            'tipo':      forms.Select(attrs={'class': 'form-select'}),
            'nit':       forms.TextInput(attrs={'class': 'form-control'}),
        }
