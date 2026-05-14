from django.contrib import admin
from .models import FactorEmision, Consumo, Emision

@admin.register(FactorEmision)
class FactorEmisionAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'subcategoria', 'valor', 'unidad', 'fuente']
    list_filter  = ['categoria']

@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ['entidad', 'factor_emision', 'alcance', 'mes', 'año', 'valor']
    list_filter  = ['alcance', 'año', 'entidad']

@admin.register(Emision)
class EmisionAdmin(admin.ModelAdmin):
    list_display = ['consumo', 'tco2e', 'factor_usado', 'fecha_calculo']
    readonly_fields = ['consumo', 'tco2e', 'factor_usado', 'fecha_calculo']
