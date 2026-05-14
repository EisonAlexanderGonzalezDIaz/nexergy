"""
recomendaciones/models.py
Modelo para las recomendaciones de energías verdes
generadas automáticamente por el motor de NEXERGY.
"""

from django.db import models
from entidades.models import Entidad


class Recomendacion(models.Model):

    VIABILIDAD_CHOICES = [
        ('ALTA',  'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA',  'Baja'),
    ]
    ESTADO_CHOICES = [
        ('PENDIENTE',    'Pendiente'),
        ('EN_ESTUDIO',   'En estudio'),
        ('EN_EJECUCION', 'En ejecución'),
        ('IMPLEMENTADA', 'Implementada'),
    ]

    entidad             = models.ForeignKey(Entidad, on_delete=models.CASCADE, related_name='recomendaciones')
    titulo              = models.CharField(max_length=200)
    descripcion         = models.TextField()
    reduccion_estimada  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Reducción estimada (tCO₂e/año)')
    costo_referencial   = models.CharField(max_length=100, verbose_name='Costo referencial (COP)', blank=True)
    viabilidad          = models.CharField(max_length=10, choices=VIABILIDAD_CHOICES, default='MEDIA')
    estado              = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_generacion    = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
        ordering            = ['-reduccion_estimada']

    def __str__(self):
        return f"{self.entidad.nombre} — {self.titulo}"
