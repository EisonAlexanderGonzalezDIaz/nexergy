"""
entidades/models.py
Define los modelos Municipio y Entidad.
Cada clase Python = una tabla en MySQL.
"""

from django.db import models


class Municipio(models.Model):
    """
    Los 11 municipios de Sabana Centro.
    Se cargan automáticamente con el fixture datos_iniciales.json.
    """
    nombre       = models.CharField(max_length=100, unique=True)
    departamento = models.CharField(max_length=100, default='Cundinamarca')

    class Meta:
        verbose_name        = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre


class Entidad(models.Model):
    """
    Alcaldía, secretaría o empresa pública de Sabana Centro
    que usa NEXERGY para medir su huella de carbono.
    """

    TIPO_CHOICES = [
        ('ALCALDIA',   'Alcaldía'),
        ('SECRETARIA', 'Secretaría'),
        ('EMPRESA',    'Empresa pública'),
        ('OTRO',       'Otro'),
    ]

    nombre    = models.CharField(max_length=200, verbose_name='Nombre de la entidad')
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,      # no permite borrar un municipio con entidades
        related_name='entidades',
        verbose_name='Municipio'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='ALCALDIA',
        verbose_name='Tipo de entidad'
    )
    nit    = models.CharField(max_length=20, unique=True, verbose_name='NIT')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Entidad'
        verbose_name_plural = 'Entidades'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.municipio})"
