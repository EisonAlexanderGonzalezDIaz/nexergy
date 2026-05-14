from django.urls import path
from . import views
app_name = 'recomendaciones'
urlpatterns = [
    path('',                      views.lista,         name='lista'),
    path('<int:pk>/estado/',      views.cambiar_estado, name='estado'),
]
