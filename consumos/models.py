"""
consumos/models.py
Modelos para registrar los consumos energéticos y
las emisiones calculadas de cada entidad.
"""

from django.db import models
from entidades.models import Entidad


class FactorEmision(models.Model):
    """
    Factores de emisión del IPCC AR6 y la UPME.
    El administrador puede actualizarlos desde el panel de Django Admin.
    Ejemplo: gasolina → 2.31 kgCO2e/litro
    """
    categoria        = models.CharField(max_length=100, verbose_name='Categoría')
    subcategoria     = models.CharField(max_length=100, verbose_name='Subcategoría')
    valor            = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Factor (kgCO2e/unidad)')
    unidad           = models.CharField(max_length=50, verbose_name='Unidad del consumo')
    fuente           = models.CharField(max_length=200, verbose_name='Fuente (IPCC/UPME)')
    año_referencia   = models.IntegerField(default=2021, verbose_name='Año de referencia')

    class Meta:
        verbose_name        = 'Factor de emisión'
        verbose_name_plural = 'Factores de emisión'
        ordering            = ['categoria', 'subcategoria']

    def __str__(self):
        return f"{self.categoria} / {self.subcategoria} — {self.valor} kgCO2e/{self.unidad}"


class Consumo(models.Model):
    """
    Registro mensual de un tipo de consumo de una entidad.
    Un consumo → un registro de emisión calculada.
    """

    ALCANCE_CHOICES = [
        (1, 'Alcance 1 — Emisiones directas (combustibles)'),
        (2, 'Alcance 2 — Energía eléctrica'),
        (3, 'Alcance 3 — Residuos y transporte'),
    ]

    entidad        = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='consumos')
    factor_emision = models.ForeignKey(FactorEmision, on_delete=models.PROTECT, verbose_name='Tipo de consumo')
    alcance        = models.IntegerField(choices=ALCANCE_CHOICES, verbose_name='Alcance GHG')
    año            = models.IntegerField(verbose_name='Año')
    mes            = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)], verbose_name='Mes')
    valor          = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cantidad consumida')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Consumo'
        verbose_name_plural = 'Consumos'
        # Evita duplicados: una entidad no puede tener dos registros del mismo tipo/mes/año
        unique_together = ('entidad', 'factor_emision', 'año', 'mes')
        ordering = ['-año', '-mes']

    def __str__(self):
        return f"{self.entidad.nombre} | {self.factor_emision.subcategoria} | {self.mes}/{self.año}"


class Emision(models.Model):
    """
    Resultado del cálculo de huella de carbono para un consumo.
    Generado automáticamente por calculadora/services.py al guardar un consumo.
    """
    consumo       = models.OneToOneField(Consumo, on_delete=models.CASCADE, related_name='emision')
    tco2e         = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Emisiones (tCO₂e)')
    factor_usado  = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Factor aplicado')
    fecha_calculo = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Emisión calculada'
        verbose_name_plural = 'Emisiones calculadas'

    def __str__(self):
        return f"{self.consumo} → {self.tco2e} tCO₂e"
