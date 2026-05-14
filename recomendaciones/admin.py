from django.contrib import admin
from .models import Recomendacion

@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display  = ['entidad', 'titulo', 'reduccion_estimada', 'viabilidad', 'estado']
    list_filter   = ['viabilidad', 'estado']
    search_fields = ['titulo', 'entidad__nombre']
