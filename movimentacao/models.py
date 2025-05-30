from django.db import models
import uuid

class Movimentacao(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        verbose_name="ID"
    )
    processo = models.ForeignKey(
        'processo.Processo',
        on_delete=models.CASCADE,
        related_name='movimentacoes',
        verbose_name="Processo"
    )
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    tipo_movimentacao = models.CharField(
        max_length=50,
        verbose_name="Tipo de Movimentação"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    responsavel = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Responsável"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    def __str__(self):
        return f"{self.tipo_movimentacao} - {self.processo}"