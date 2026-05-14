from django.contrib import admin
from .models import Municipio, Entidad

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'departamento']

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'municipio', 'tipo', 'nit', 'activo']
    list_filter   = ['municipio', 'tipo', 'activo']
    search_fields = ['nombre', 'nit']
