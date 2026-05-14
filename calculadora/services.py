"""
calculadora/services.py
─────────────────────────────────────────────────────────
Motor de cálculo de huella de carbono de NEXERGY.

Este módulo NO depende de Django views ni templates,
por eso se puede probar con unittest sin levantar el servidor.

Fórmula base:
  Emisiones (tCO₂e) = Consumo (unidad) × Factor de emisión (kgCO₂e/unidad) / 1000
─────────────────────────────────────────────────────────
"""

from decimal import Decimal
from django.db.models import Sum
from consumos.models import Consumo, Emision


def calcular_huella(consumo: Consumo) -> Emision:
    """
    Calcula las emisiones de un registro de consumo y
    guarda (o actualiza) el resultado en la tabla Emision.

    Parámetros:
        consumo: instancia de Consumo ya guardada en la BD.

    Retorna:
        instancia de Emision con el resultado en tCO₂e.
    """
    factor = Decimal(str(consumo.factor_emision.valor))  # kgCO2e por unidad
    valor  = Decimal(str(consumo.valor))                  # cantidad consumida

    # Convertimos de kg a toneladas dividiendo entre 1000
    tco2e = (valor * factor) / Decimal('1000')

    # update_or_create: crea la emisión si no existe, la actualiza si ya existe
    emision, _ = Emision.objects.update_or_create(
        consumo=consumo,
        defaults={
            'tco2e':        tco2e,
            'factor_usado': factor,
        }
    )
    return emision


def obtener_resumen_entidad(entidad_id: int, año: int) -> dict:
    """
    Calcula el resumen anual de emisiones de una entidad,
    desglosado por alcance.

    Retorna un dict con la estructura:
    {
        'total': Decimal,
        'alcance_1': Decimal,
        'alcance_2': Decimal,
        'alcance_3': Decimal,
        'por_categoria': [ {'categoria': str, 'total': Decimal}, ... ]
    }
    """
    consumos = Consumo.objects.filter(entidad_id=entidad_id, año=año)

    # Suma de tCO2e agrupada por alcance usando el ORM de Django
    def suma_alcance(n):
        resultado = (
            Emision.objects
            .filter(consumo__entidad_id=entidad_id, consumo__año=año, consumo__alcance=n)
            .aggregate(total=Sum('tco2e'))
        )
        return resultado['total'] or Decimal('0')

    alcance_1 = suma_alcance(1)
    alcance_2 = suma_alcance(2)
    alcance_3 = suma_alcance(3)
    total     = alcance_1 + alcance_2 + alcance_3

    # Desglose por categoría de consumo
    por_categoria = []
    categorias = consumos.values_list('factor_emision__categoria', flat=True).distinct()
    for cat in categorias:
        t = (
            Emision.objects
            .filter(consumo__entidad_id=entidad_id, consumo__año=año, consumo__factor_emision__categoria=cat)
            .aggregate(total=Sum('tco2e'))
        )
        por_categoria.append({'categoria': cat, 'total': t['total'] or Decimal('0')})

    # Ordenar de mayor a menor para mostrar el top primero
    por_categoria.sort(key=lambda x: x['total'], reverse=True)

    return {
        'total':         total,
        'alcance_1':     alcance_1,
        'alcance_2':     alcance_2,
        'alcance_3':     alcance_3,
        'por_categoria': por_categoria,
    }


def obtener_tendencia_mensual(entidad_id: int, año: int) -> list:
    """
    Retorna una lista de 12 elementos (uno por mes) con
    las emisiones totales mensuales de la entidad.

    Formato: [{'mes': 1, 'tco2e': Decimal}, ..., {'mes': 12, 'tco2e': Decimal}]
    Meses sin datos quedan en 0.
    """
    tendencia = []
    for mes in range(1, 13):
        resultado = (
            Emision.objects
            .filter(consumo__entidad_id=entidad_id, consumo__año=año, consumo__mes=mes)
            .aggregate(total=Sum('tco2e'))
        )
        tendencia.append({
            'mes':   mes,
            'tco2e': float(resultado['total'] or 0),
        })
    return tendencia


def obtener_comparativa_regional(año: int) -> list:
    """
    Retorna el total de emisiones de cada municipio en un año,
    ordenado de mayor a menor. Usado en la vista comparativa regional.

    Formato: [{'municipio': str, 'total': float}, ...]
    """
    from entidades.models import Municipio

    resultado = []
    for municipio in Municipio.objects.all():
        total = (
            Emision.objects
            .filter(consumo__entidad__municipio=municipio, consumo__año=año)
            .aggregate(total=Sum('tco2e'))
        )
        resultado.append({
            'municipio': municipio.nombre,
            'total':     float(total['total'] or 0),
        })

    resultado.sort(key=lambda x: x['total'], reverse=True)
    return resultado
