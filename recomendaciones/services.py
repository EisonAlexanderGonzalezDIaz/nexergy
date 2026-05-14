"""
recomendaciones/services.py
─────────────────────────────────────────────────
Genera recomendaciones de energías verdes según
la fuente de mayor emisión de la entidad.
─────────────────────────────────────────────────
"""

from decimal import Decimal
from recomendaciones.models import Recomendacion


# Catálogo de recomendaciones por categoría de mayor emisión
CATALOGO = {
    'Energía eléctrica': [
        {
            'titulo': 'Instalación de paneles solares fotovoltaicos',
            'descripcion': (
                'Instalar un sistema de paneles solares en el techo de la sede principal. '
                'Un sistema de 20 kWp puede generar ~26.000 kWh/año en Cundinamarca, '
                'reduciendo significativamente el consumo de red eléctrica.'
            ),
            'reduccion_base': Decimal('8.5'),
            'costo_referencial': '$80.000.000 – $120.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Sustitución de iluminación por tecnología LED',
            'descripcion': (
                'Reemplazar toda la iluminación fluorescente por LED de alta eficiencia. '
                'El consumo de iluminación puede reducirse hasta un 60%, con retorno '
                'de inversión en 2–3 años.'
            ),
            'reduccion_base': Decimal('3.2'),
            'costo_referencial': '$15.000.000 – $30.000.000 COP',
            'viabilidad': 'ALTA',
        },
    ],
    'Gasolina': [
        {
            'titulo': 'Electrificación parcial de la flota vehicular',
            'descripcion': (
                'Sustituir vehículos de combustión por vehículos eléctricos o híbridos '
                'en la flota municipal. Colombia tiene incentivos tributarios para la compra '
                'de vehículos eléctricos (exención de IVA y ArAncel).'
            ),
            'reduccion_base': Decimal('12.0'),
            'costo_referencial': '$150.000.000 – $300.000.000 COP por vehículo',
            'viabilidad': 'MEDIA',
        },
        {
            'titulo': 'Programa de conducción eficiente',
            'descripcion': (
                'Capacitar a los conductores en técnicas de eco-driving. '
                'Esta medida puede reducir el consumo de combustible entre un 10–15% '
                'sin ninguna inversión en infraestructura.'
            ),
            'reduccion_base': Decimal('2.5'),
            'costo_referencial': '$2.000.000 – $5.000.000 COP',
            'viabilidad': 'ALTA',
        },
    ],
    'ACPM': [
        {
            'titulo': 'Sustitución de ACPM por biocombustible B20',
            'descripcion': (
                'Mezclar ACPM con un 20% de biodiesel (B20) en la flota diésel. '
                'Esta medida reduce las emisiones netas de CO₂ en aproximadamente '
                'un 15% y es compatible con motores actuales.'
            ),
            'reduccion_base': Decimal('5.0'),
            'costo_referencial': '$0 – diferencia de precio en el surtidor',
            'viabilidad': 'ALTA',
        },
    ],
    'Residuos sólidos': [
        {
            'titulo': 'Implementación de compostaje institucional',
            'descripcion': (
                'Instalar una unidad de compostaje para residuos orgánicos de cocinas '
                'y jardines. El compost generado puede usarse en zonas verdes, '
                'reduciendo residuos al relleno sanitario hasta un 30%.'
            ),
            'reduccion_base': Decimal('4.0'),
            'costo_referencial': '$8.000.000 – $15.000.000 COP',
            'viabilidad': 'ALTA',
        },
        {
            'titulo': 'Programa de separación en la fuente y reciclaje',
            'descripcion': (
                'Implementar puntos ecológicos con contenedores diferenciados '
                '(orgánico, reciclable, no reciclable) y un programa de sensibilización '
                'para funcionarios. Meta: reducir residuos al relleno en un 25%.'
            ),
            'reduccion_base': Decimal('2.8'),
            'costo_referencial': '$5.000.000 – $10.000.000 COP',
            'viabilidad': 'ALTA',
        },
    ],
    'Gas natural': [
        {
            'titulo': 'Instalación de calentadores solares de agua',
            'descripcion': (
                'Sustituir calentadores de agua a gas por sistemas solares térmicos. '
                'En Cundinamarca, un sistema de 200 litros/día puede cubrir el 60–70% '
                'de la demanda de agua caliente.'
            ),
            'reduccion_base': Decimal('3.5'),
            'costo_referencial': '$12.000.000 – $20.000.000 COP',
            'viabilidad': 'MEDIA',
        },
    ],
}


def generar_recomendaciones(entidad, resumen: dict) -> list:
    """
    Genera recomendaciones para una entidad basándose en su
    resumen de emisiones. Borra las recomendaciones 'PENDIENTE'
    anteriores y crea nuevas.

    Parámetros:
        entidad: instancia de Entidad
        resumen: dict retornado por calculadora.services.obtener_resumen_entidad()

    Retorna:
        lista de instancias de Recomendacion creadas
    """
    # Eliminar recomendaciones pendientes anteriores para regenerarlas
    Recomendacion.objects.filter(entidad=entidad, estado='PENDIENTE').delete()

    creadas = []
    categorias_ordenadas = resumen.get('por_categoria', [])

    for item in categorias_ordenadas[:3]:   # top 3 fuentes de emisión
        categoria = item['categoria']
        total_cat = item['total']

        if categoria not in CATALOGO:
            continue

        for plantilla in CATALOGO[categoria]:
            # Escala la reducción estimada proporcionalmente al volumen real
            escala = float(total_cat) / 10.0 if float(total_cat) > 0 else 1.0
            reduccion = plantilla['reduccion_base'] * Decimal(str(min(escala, 3.0)))

            rec = Recomendacion.objects.create(
                entidad            = entidad,
                titulo             = plantilla['titulo'],
                descripcion        = plantilla['descripcion'],
                reduccion_estimada = reduccion.quantize(Decimal('0.01')),
                costo_referencial  = plantilla['costo_referencial'],
                viabilidad         = plantilla['viabilidad'],
                estado             = 'PENDIENTE',
            )
            creadas.append(rec)

    return creadas
