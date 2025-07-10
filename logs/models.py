# logs/models.py
from django.conf import settings
from django.db import models

class ConsultaLog(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    numero_processo = models.CharField(max_length=50, blank=True)
    metodo   = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Log de consulta'
        verbose_name_plural = 'Logs de consulta'

    def __str__(self):
        return f'{self.usuario or "anon"} – {self.numero_processo} – {self.timestamp:%d/%m/%Y %H:%M}'
