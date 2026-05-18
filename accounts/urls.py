from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',           views.login_view,      name='login'),
    path('logout/',          views.logout_view,     name='logout'),
    path('registro/',        views.registro_view,   name='registro'),
    path('check-username/',  views.check_username,  name='check_username'),
    path('check-email/',     views.check_email,     name='check_email'),
]