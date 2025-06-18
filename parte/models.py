import uuid
from django.db import models

class Parte(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        unique=True, 
        db_index=True,
        default=uuid.uuid4,
        verbose_name="ID",
    )
    processo = models.ForeignKey(
        'processo.Processo',
        on_delete=models.CASCADE,
        related_name='partes',
        verbose_name="Processo"
    )
    nome = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Nome da Parte"
    )

    TIPO_PARTE_CHOICES = [
        ('AUT', 'Autor'),
        ('REU', 'Réu'),
        ('LIA', 'Litisconsorte Ativo'),
        ('LIP', 'Litisconsorte Passivo'),
        ('ASS', 'Assistente'),
        ('INE', 'Interveniente'),
    ]
    tipo_parte = models.CharField(
        max_length=3,
        choices=TIPO_PARTE_CHOICES,
        verbose_name="Tipo de Parte"
    )
    documento = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        verbose_name="CPF/CNPJ"
    )
    created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )
        