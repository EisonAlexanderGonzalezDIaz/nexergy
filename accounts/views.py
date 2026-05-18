from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def registro_view(request):
    if request.method == 'POST':
        username         = request.POST.get('username')
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        first_name       = request.POST.get('first_name')
        last_name        = request.POST.get('last_name')
        municipio_nombre = request.POST.get('municipio')

        # Validar usuario duplicado
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username_exists')
            return redirect('accounts:login')

        # Validar correo duplicado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email_exists')
            return redirect('accounts:login')

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )

        # Crear perfil automáticamente
        from entidades.models import Entidad, Municipio
        from .models import PerfilUsuario

        municipio = Municipio.objects.filter(
            nombre__iexact=municipio_nombre
        ).first()

        entidad = Entidad.objects.filter(
            municipio=municipio
        ).first() if municipio else None

        PerfilUsuario.objects.create(
            usuario=user,
            rol='FUNCIONARIO',
            entidad=entidad
        )

        messages.success(
            request,
            f'¡Bienvenido {first_name}! Tu cuenta ha sido creada. Ya puedes ingresar.'
        )
        return redirect('accounts:login')

    return redirect('accounts:login')

from django.http import JsonResponse

def check_username(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def check_email(request):
    email = request.GET.get('email', '')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})