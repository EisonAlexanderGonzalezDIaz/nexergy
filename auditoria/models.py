"""auditoria/models.py — Registro de actividad de usuarios."""
from django.db import models
from django.contrib.auth.models import User


class RegistroSesion(models.Model):
    usuario         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones')
    inicio_sesion   = models.DateTimeField(auto_now_add=True)
    fin_sesion      = models.DateTimeField(null=True, blank=True)
    duracion_minutos= models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    ip              = models.GenericIPAddressField(null=True, blank=True)
    activa          = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Registro de Sesión'
        verbose_name_plural = 'Registros de Sesiones'
        ordering            = ['-inicio_sesion']

    def __str__(self):
        return f"{self.usuario.username} — {self.inicio_sesion.strftime('%d/%m/%Y %H:%M')}"

    def cerrar(self):
        import datetime
        from django.utils import timezone
        self.fin_sesion = timezone.now()
        delta = self.fin_sesion - self.inicio_sesion
        self.duracion_minutos = round(delta.total_seconds() / 60, 2)
        self.activa = False
        self.save()