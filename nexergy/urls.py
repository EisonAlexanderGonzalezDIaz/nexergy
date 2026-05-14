"""
nexergy/urls.py
Router principal — conecta las URLs de cada app.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Panel de administración de Django (solo para administradores)
    path('admin/', admin.site.urls),

    # Redirige la raíz al dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # URLs de cada app
    path('accounts/',       include('accounts.urls')),
    path('entidades/',      include('entidades.urls')),
    path('consumos/',       include('consumos.urls')),
    path('dashboard/',      include('dashboard.urls')),
    path('recomendaciones/',include('recomendaciones.urls')),
    path('reportes/',       include('reportes.urls')),
]
