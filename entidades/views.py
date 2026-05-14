from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Entidad, Municipio
from .forms import EntidadForm

@login_required
def lista(request):
    entidades = Entidad.objects.select_related('municipio').filter(activo=True)
    return render(request, 'entidades/lista.html', {'entidades': entidades})

@login_required
def nueva(request):
    if request.method == 'POST':
        form = EntidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entidad registrada correctamente.')
            return redirect('entidades:lista')
    else:
        form = EntidadForm()
    return render(request, 'entidades/form.html', {'form': form, 'titulo': 'Nueva entidad'})

@login_required
def editar(request, pk):
    entidad = get_object_or_404(Entidad, pk=pk)
    if request.method == 'POST':
        form = EntidadForm(request.POST, instance=entidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entidad actualizada.')
            return redirect('entidades:lista')
    else:
        form = EntidadForm(instance=entidad)
    return render(request, 'entidades/form.html', {'form': form, 'titulo': 'Editar entidad'})
