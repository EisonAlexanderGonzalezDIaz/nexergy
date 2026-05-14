from django.urls import path
from . import views
app_name = 'reportes'
urlpatterns = [
    path('pdf/', views.generar_pdf, name='pdf'),
]
