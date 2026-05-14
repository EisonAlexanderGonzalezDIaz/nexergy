"""consumos/views.py"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Consumo
from .forms import ConsumoForm
from calculadora.services import calcular_huella
from entidades.models import Entidad


@login_required
def lista_consumos(request):
    """Muestra los consumos registrados de la entidad del usuario."""
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        messages.error(request, 'No tienes una entidad asignada. Contacta al administrador.')
        return redirect('dashboard:index')

    consumos = Consumo.objects.filter(entidad=entidad).select_related('factor_emision', 'emision')
    return render(request, 'consumos/lista.html', {'consumos': consumos, 'entidad': entidad})


@login_required
def nuevo_consumo(request):
    """Formulario para registrar un nuevo consumo y calcular su emisión."""
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        messages.error(request, 'No tienes una entidad asignada.')
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            consumo = form.save(commit=False)
            consumo.entidad = entidad
            consumo.alcance = consumo.factor_emision.categoria  # se asigna por factor
            # Determinar alcance según categoría del factor
            cat = consumo.factor_emision.categoria.lower()
            if 'eléctric' in cat or 'electri' in cat:
                consumo.alcance = 2
            elif 'residuo' in cat:
                consumo.alcance = 3
            else:
                consumo.alcance = 1
            consumo.save()
            # Calcular la huella de carbono automáticamente
            emision = calcular_huella(consumo)
            messages.success(
                request,
                f'Consumo guardado. Emisión calculada: {emision.tco2e:.4f} tCO₂e'
            )
            return redirect('consumos:nuevo')
    else:
        form = ConsumoForm()

    return render(request, 'consumos/nuevo.html', {'form': form, 'entidad': entidad})


@login_required
def eliminar_consumo(request, pk):
    consumo = get_object_or_404(Consumo, pk=pk, entidad=request.user.perfil.entidad)
    if request.method == 'POST':
        consumo.delete()
        messages.success(request, 'Consumo eliminado.')
    return redirect('consumos:lista')
