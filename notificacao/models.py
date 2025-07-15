import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from processo.models import Processo
from movimentacao.models import Movimentacao


class Notificacao(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID da Notificação"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name="Usuário"
    )
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name="Processo"
    )
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notificacoes',
        verbose_name="Movimentação Associada"
    )
    tipo_notificacao = models.CharField(
        max_length=255,
        verbose_name="Tipo da Notificação"
    )
    lida = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Lida"
    )
    enviada = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Enviada"
    )
    data_envio = models.DateTimeField(
        null=True, blank=True, verbose_name="Data de Envio")
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        # por numero_processo 
        return f"Notificação para {self.usuario.username} sobre o processo {self.processo.numero_processo}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-created_at']