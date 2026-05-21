"""dashboard/views.py"""
import json
import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from recomendaciones.services import generar_recomendaciones
from calculadora.services import (
    obtener_resumen_entidad,
    obtener_comparativa_regional,
    obtener_tendencia_mensual,
)

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    contacto_ok = False
    if request.method == 'POST' and request.POST.get('form_contacto'):
        nombre   = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        email    = request.POST.get('email', '')
        telefono = request.POST.get('telefono', '')
        motivo   = request.POST.get('motivo', '')
        mensaje  = request.POST.get('mensaje', '')

        try:
            from django.core.mail import send_mail
            from django.conf import settings
            send_mail(
                subject=f'[NEXERGY] Contacto: {motivo} — {nombre} {apellido}',
                message=f'Nombre: {nombre} {apellido}\nCorreo: {email}\nTeléfono: {telefono}\nMotivo: {motivo}\n\nMensaje:\n{mensaje}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception:
            pass

        contacto_ok = True
    return render(request, 'landing.html', {'contacto_ok': contacto_ok})

@login_required
def index(request):
    """Vista principal del dashboard con KPIs y gráficas."""
    año_actual = datetime.date.today().year
    año = int(request.GET.get('año', año_actual))

    try:
        entidad = request.user.perfil.entidad
    except Exception:
        entidad = None

    resumen   = obtener_resumen_entidad(entidad.id, año) if entidad else {}
    tendencia = obtener_tendencia_mensual(entidad.id, año) if entidad else []
    comparativa = obtener_comparativa_regional(año)

    # Generar/actualizar recomendaciones si hay datos
    if entidad and resumen.get('total', 0) > 0:
        generar_recomendaciones(entidad, resumen)

    # Serializar datos para Chart.js (JSON)
    tendencia_labels = [f'Mes {t["mes"]}' for t in tendencia]
    tendencia_datos  = [t['tco2e'] for t in tendencia]
    comp_labels = [c['municipio'] for c in comparativa]
    comp_datos  = [c['total'] for c in comparativa]

    # Años disponibles para el selector
    años = list(range(2020, año_actual + 1))

    context = {
        'entidad':          entidad,
        'resumen':          resumen,
        'año':              año,
        'años':             años,
        'tendencia_labels': json.dumps(tendencia_labels),
        'tendencia_datos':  json.dumps(tendencia_datos),
        'comp_labels':      json.dumps(comp_labels),
        'comp_datos':       json.dumps(comp_datos),
        # Colores semáforo para el donut chart
        'alcance_datos':    json.dumps([
            float(resumen.get('alcance_1', 0)),
            float(resumen.get('alcance_2', 0)),
            float(resumen.get('alcance_3', 0)),
        ]),
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def home(request):
    return render(request, 'home.html')