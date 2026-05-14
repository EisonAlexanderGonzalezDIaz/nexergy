"""consumos/urls.py"""
from django.urls import path
from . import views
app_name = 'consumos'
urlpatterns = [
    path('',              views.lista_consumos,  name='lista'),
    path('nuevo/',        views.nuevo_consumo,   name='nuevo'),
    path('eliminar/<int:pk>/', views.eliminar_consumo, name='eliminar'),
]
