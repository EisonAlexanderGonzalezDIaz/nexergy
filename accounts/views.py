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
        tipo_entidad     = request.POST.get('tipo_entidad')
        municipio_nombre = request.POST.get('municipio')

        # Verificar usuario duplicado
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
            return redirect('accounts:login')

        # Crear usuario activo de una vez
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True  # activo de inmediato
        )

        # Crear perfil con entidad asignada automáticamente
        try:
            from entidades.models import Entidad, Municipio
            from .models import PerfilUsuario

            # Buscar municipio
            municipio = Municipio.objects.filter(
                nombre__icontains=municipio_nombre
            ).first()

            # Buscar entidad por municipio y tipo
            entidad = None
            if municipio:
                entidad = Entidad.objects.filter(
                    municipio=municipio
                ).first()

            # Crear perfil con rol funcionario por defecto
            PerfilUsuario.objects.create(
                user=user,
                rol='funcionario',
                entidad=entidad
            )

        except Exception:
            # Si falla la asignación de entidad igual se crea el usuario
            pass

        messages.success(
            request,
            f'¡Bienvenido {first_name}! Tu cuenta ha sido creada. Ya puedes ingresar.'
        )
        return redirect('accounts:login')

    return redirect('accounts:login')