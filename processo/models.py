from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

# ───────────────────────────────────────────────
# Choices para a situação do processo
# ───────────────────────────────────────────────
class SituacaoProcesso(models.TextChoices):
    # Fases Iniciais
    CADASTRADO = 'CAD', 'Cadastrado'
    DISTRIBUIDO = 'DIS', 'Distribuído'
    AGUARDANDO_CITACAO = 'CIT', 'Aguardando Citação'
    IMPULSIONADO = 'IMP', 'Impulsionado'
    # Andamento
    EM_PREPARO = 'PRE', 'Em Preparo'
    EM_PAUTA_EMBARGOS = 'PEC', 'Em Pauta para Embargos'
    RECURSAL = 'REC', 'Recursal'
    HOMOLOGADO = 'HOM', 'Homologado'
    # Suspensões
    SUSPENSO = 'SUS', 'Suspenso'
    SUSPENSO_AUSENCIA_PARTES = 'AUS', 'Suspenso por Ausência de Partes'
    SUSPENSO_PERICIA = 'PER', 'Suspenso por Perícia'
    # Finalizações
    ARQUIVADO = 'ARQ', 'Arquivado'
    BAIXADO = 'BAI', 'Baixado'
    JULGADO = 'JUL', 'Julgado'
    EXTINTO = 'EXT', 'Extinto'
    CUMPRIDO = 'CUM', 'Cumprido'
    LIQUIDADO = 'LIQ', 'Liquidado'
    # Situações Especiais
    DESMEMBRADO = 'DES', 'Desmembrado'
    INCIDENTE_PROCESSUAL = 'INC', 'Incidente Processual'
    INTERVENCAO_TERCEIRO = 'INT', 'Intervenção de Terceiro'
    UNIFICADO = 'UNI', 'Unificado'

# ───────────────────────────────────────────────
# Modelo principal do processo
# ───────────────────────────────────────────────
class Processo(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        db_index=True,
        default=uuid.uuid4,
        verbose_name="ID",
    )

    # Número CNJ completo — ex.: 1234567-89.2023.8.26.0100
    numero_processo = models.CharField(
        max_length=26,
        unique=True,
        db_index=True,
        verbose_name="Número do Processo",
        validators=[
            RegexValidator(
                regex=r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$',
                message="Formato inválido. Use '1234567-89.2023.8.26.0100'."
            )
        ],
    )

    # ────── Novos campos para simular busca por pessoa ──────
    parte_nome = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Nome da Parte Principal",
    )
    parte_cpf = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="CPF no formato '000.000.000-00'.",
            )
        ],
        verbose_name="CPF da Parte Principal",
    )
    # ─────────────────────────────────────────────────────────

    tribunal = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Tribunal",
    )
    classe_processual = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Classe Processual",
    )
    assunto = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Assunto",
    )
    data_distribuicao = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Distribuição",
    )
    orgao_julgador = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Órgão Julgador",
    )
    valor_causa = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Valor da Causa",
    )
    situacao_atual = models.CharField(
        max_length=3,
        choices=SituacaoProcesso.choices,
        default=SituacaoProcesso.CADASTRADO,
        null=True,
        blank=True,
        verbose_name="Situação Atual",
    )
    ultima_atualizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Atualização",
    )
    # (mantido) — remova blank/null quando o app de usuários estiver pronto
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Data de Criação",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização",
    )

    def __str__(self):
        return f"{self.numero_processo} – {self.parte_nome or 'Parte não definida'}"
