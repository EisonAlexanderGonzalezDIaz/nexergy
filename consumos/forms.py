"""consumos/forms.py"""
from django import forms
from .models import Consumo, FactorEmision
from django.core.exceptions import ValidationError
import datetime

MESES = [(i, f'{i:02d}') for i in range(1, 13)]
AÑOS  = [(y, str(y)) for y in range(2020, datetime.date.today().year + 2)]

class ConsumoForm(forms.ModelForm):
    año = forms.ChoiceField(choices=AÑOS, label='Año')
    mes = forms.ChoiceField(choices=MESES, label='Mes')

    class Meta:
        model   = Consumo
        fields  = ['factor_emision', 'año', 'mes', 'valor']
        labels  = {
            'factor_emision': 'Tipo de consumo',
            'valor':          'Cantidad',
        }
        widgets = {
            'factor_emision': forms.Select(attrs={'class': 'form-select'}),
            'valor':          forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                continue
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-select'

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise ValidationError('El valor debe ser mayor que cero.')
        return valor
