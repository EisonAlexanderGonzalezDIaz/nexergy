from django.contrib import admin
from .models import RegistroSesion


@admin.register(RegistroSesion)
class RegistroSesionAdmin(admin.ModelAdmin):
    list_display  = ['usuario', 'inicio_sesion', 'fin_sesion', 'duracion_minutos', 'ip', 'activa']
    list_filter   = ['activa', 'usuario']
    search_fields = ['usuario__username']
    readonly_fields = ['inicio_sesion', 'fin_sesion', 'duracion_minutos', 'ip']