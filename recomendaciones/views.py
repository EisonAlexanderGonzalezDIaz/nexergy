"""recomendaciones/views.py"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recomendacion


@login_required
def lista(request):
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        entidad = None

    recs = Recomendacion.objects.filter(entidad=entidad) if entidad else []
    return render(request, 'recomendaciones/lista.html', {'recomendaciones': recs, 'entidad': entidad})


@login_required
def cambiar_estado(request, pk):
    """Permite al funcionario actualizar el estado de una recomendación."""
    rec = get_object_or_404(Recomendacion, pk=pk, entidad=request.user.perfil.entidad)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        estados_validos = [e[0] for e in Recomendacion.ESTADO_CHOICES]
        if nuevo_estado in estados_validos:
            rec.estado = nuevo_estado
            rec.save()
            messages.success(request, f'Estado actualizado a: {rec.get_estado_display()}')
    return redirect('recomendaciones:lista')
