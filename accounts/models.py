"""
accounts/models.py
Extiende el usuario de Django con un perfil que incluye
el rol y la entidad a la que pertenece.
"""

from django.db import models
from django.contrib.auth.models import User
from entidades.models import Entidad


class PerfilUsuario(models.Model):
    """
    Perfil adicional del usuario.
    Django ya maneja usuario/contraseña; aquí agregamos rol y entidad.
    """

    ROL_CHOICES = [
        ('ADMIN',       'Administrador'),
        ('FUNCIONARIO', 'Funcionario Municipal'),
        ('CONSULTOR',   'Consultor / Auditor'),
    ]

    # OneToOneField: cada User tiene exactamente un PerfilUsuario
    usuario  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol      = models.CharField(max_length=20, choices=ROL_CHOICES, default='FUNCIONARIO')
    entidad  = models.ForeignKey(
        Entidad,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Entidad asignada'
    )

    class Meta:
        verbose_name        = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} — {self.get_rol_display()}"

    def es_admin(self):
        return self.rol == 'ADMIN'

    def es_funcionario(self):
        return self.rol == 'FUNCIONARIO'

    def es_consultor(self):
        return self.rol == 'CONSULTOR'
