from django.contrib.auth.models import User

def registro_view(request):
    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password   = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
            return redirect('accounts:login')

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            is_active=False  # espera aprobación del admin
        )
        messages.success(request, 'Cuenta creada. Espera que el administrador la active.')
        return redirect('accounts:login')

    return redirect('accounts:login')