"""recomendaciones/views.py"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recomendacion
from consumos.models import Consumo
import datetime


# Catálogo de recomendaciones por tipo de consumo
CATALOGO = {
    'electricidad': [
        {
            'titulo': 'Instalación de paneles solares fotovoltaicos',
            'descripcion': 'Instalar un sistema de paneles solares en la sede principal. Un sistema de 20 kWp puede generar ~26.000 kWh/año en Cundinamarca, reduciendo significativamente el consumo de red eléctrica y las emisiones de Alcance 2.',
            'reduccion_base': 1.3,
            'costo': '$80.000.000 – $120.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Sustitución de iluminación por tecnología LED',
            'descripcion': 'Reemplazar toda la iluminación fluorescente por LED de alta eficiencia. El consumo de iluminación puede reducirse hasta un 60%, con retorno de inversión en 2–3 años.',
            'reduccion_base': 0.5,
            'costo': '$15.000.000 – $30.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Sistema de gestión energética (SGE)',
            'descripcion': 'Implementar un sistema de monitoreo y control del consumo eléctrico en tiempo real. Permite identificar equipos de alto consumo y establecer políticas de ahorro energético institucional.',
            'reduccion_base': 0.4,
            'costo': '$20.000.000 – $45.000.000 COP',
            'viabilidad': 'MEDIA',
        },
    ],
    'combustibles': [
        {
            'titulo': 'Renovación de flota vehicular a vehículos eléctricos',
            'descripcion': 'Reemplazar progresivamente los vehículos de combustión interna por vehículos eléctricos o híbridos. Colombia cuenta con incentivos tributarios para la compra de vehículos eléctricos (Ley 1964 de 2019).',
            'reduccion_base': 2.1,
            'costo': '$80.000.000 – $200.000.000 COP por vehículo',
            'viabilidad': 'MEDIA',
        },
        {
            'titulo': 'Plan de movilidad sostenible institucional',
            'descripcion': 'Implementar políticas de carpooling, teletrabajo y uso de transporte público para reducir el uso de vehículos institucionales. Puede reducir hasta un 30% las emisiones de Alcance 1 sin inversión en infraestructura.',
            'reduccion_base': 0.8,
            'costo': '$2.000.000 – $8.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Conversión de calderas a gas natural o biomasa',
            'descripcion': 'Si la entidad usa ACPM o gasolina en calderas o generadores, la conversión a gas natural puede reducir las emisiones hasta en un 25%. La biomasa es una alternativa carbono-neutral.',
            'reduccion_base': 1.2,
            'costo': '$15.000.000 – $50.000.000 COP',
            'viabilidad': 'MEDIA',
        },
    ],
    'residuos': [
        {
            'titulo': 'Implementación de compostaje institucional',
            'descripcion': 'Instalar un sistema de compostaje para residuos orgánicos generados en la entidad. El compostaje evita la descomposición anaeróbica en rellenos sanitarios, principal fuente de metano (CH₄) de Alcance 3.',
            'reduccion_base': 12.0,
            'costo': '$8.000.000 – $15.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Programa de separación en la fuente y reciclaje',
            'descripcion': 'Implementar un programa estructurado de separación de residuos sólidos en la fuente. El reciclaje de papel, plástico, vidrio y metal puede desviar hasta un 40% de los residuos del relleno sanitario.',
            'reduccion_base': 8.4,
            'costo': '$5.000.000 – $10.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Política de cero papel y digitalización',
            'descripcion': 'Implementar procesos digitales para eliminar el uso de papel en la entidad. Cada tonelada de papel reciclado evita 2.5 tCO₂e y reduce los costos operativos a largo plazo.',
            'reduccion_base': 3.2,
            'costo': '$5.000.000 – $20.000.000 COP',
            'viabilidad': 'ALTA',
        },
    ],
}


def generar_recomendaciones(entidad):
    """Genera recomendaciones basadas en los consumos reales de la entidad."""
    año_actual = datetime.date.today().year
    consumos = Consumo.objects.filter(
        entidad=entidad,
        año__in=[año_actual, año_actual - 1]
    ).select_related('factor_emision')

    if not consumos.exists():
        return

    # Detectar tipos de consumo de la entidad
    tiene_electricidad = consumos.filter(factor_emision__categoria__icontains='electric').exists() or \
                         consumos.filter(factor_emision__subcategoria__icontains='electric').exists() or \
                         consumos.filter(alcance=2).exists()

    tiene_combustibles = consumos.filter(alcance=1).exists()
    tiene_residuos     = consumos.filter(alcance=3).exists()

    # Si no detecta nada específico genera de todos los tipos
    if not tiene_electricidad and not tiene_combustibles and not tiene_residuos:
        tiene_electricidad = True
        tiene_combustibles = True
        tiene_residuos     = True

    # Eliminar recomendaciones anteriores de esta entidad
    Recomendacion.objects.filter(entidad=entidad).delete()

    # Generar nuevas recomendaciones
    nuevas = []
    if tiene_electricidad:
        for rec in CATALOGO['electricidad']:
            nuevas.append(Recomendacion(
                entidad=entidad,
                titulo=rec['titulo'],
                descripcion=rec['descripcion'],
                reduccion_estimada=rec['reduccion_base'],
                costo_referencial=rec['costo'],
                viabilidad=rec['viabilidad'],
            ))
    if tiene_combustibles:
        for rec in CATALOGO['combustibles']:
            nuevas.append(Recomendacion(
                entidad=entidad,
                titulo=rec['titulo'],
                descripcion=rec['descripcion'],
                reduccion_estimada=rec['reduccion_base'],
                costo_referencial=rec['costo'],
                viabilidad=rec['viabilidad'],
            ))
    if tiene_residuos:
        for rec in CATALOGO['residuos']:
            nuevas.append(Recomendacion(
                entidad=entidad,
                titulo=rec['titulo'],
                descripcion=rec['descripcion'],
                reduccion_estimada=rec['reduccion_base'],
                costo_referencial=rec['costo'],
                viabilidad=rec['viabilidad'],
            ))

    Recomendacion.objects.bulk_create(nuevas)


@login_required
def lista(request):
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        entidad = None

    if entidad:
        # Regenerar recomendaciones si no hay o si el usuario lo solicita
        recs = Recomendacion.objects.filter(entidad=entidad)
        if not recs.exists() or request.GET.get('regenerar'):
            generar_recomendaciones(entidad)
            recs = Recomendacion.objects.filter(entidad=entidad)
    else:
        recs = []

    return render(request, 'recomendaciones/lista.html', {
        'recomendaciones': recs,
        'entidad': entidad
    })


@login_required
def cambiar_estado(request, pk):
    rec = get_object_or_404(Recomendacion, pk=pk, entidad=request.user.perfil.entidad)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        estados_validos = [e[0] for e in Recomendacion.ESTADO_CHOICES]
        if nuevo_estado in estados_validos:
            rec.estado = nuevo_estado
            rec.save()
            messages.success(request, f'Estado actualizado a: {rec.get_estado_display()}')
    return redirect('recomendaciones:lista')