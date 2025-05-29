from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid


class Processo(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        editable=False, 
        unique=True, 
        default=uuid.uuid4,
        verbose_name="ID",
    )
    numero_processo = models.CharField(
        max_length=25,
        unique=True,
        verbose_name="Número do Processo",
        validators=[
            RegexValidator(
                regex=r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$',
                message="Formato inválido. Use '1234567-89.2023.0001'."
            )
        ]
    )
    tribunal = models.ForeignKey(    #adc o tribunal quando ele tiver pronto
        'Tribunal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tribunal"
    )
    classe_processual = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Classe Processual"
    )
    assunto = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Assunto"
    )
    data_distribuicao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Distribuição"
    )
    orgao_julgador = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        verbose_name="Órgão Julgador"
    )
    valor_causa = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True,
        verbose_name="Valor da Causa"
    )
    
    SITUACAO_CHOICES = [    # pesquisei todas as siglas, talvez precise de ajustes
                        
        # Fases Iniciais
        ('CAD', 'Cadastrado'),
        ('DIS', 'Distribuído'),
        ('CIT', 'Aguardando Citação'),
        ('IMP', 'Impulsionado'),
        
        # Andamento
        ('PRE', 'Em Preparo'),
        ('PEC', 'Em Pauta para Embargos'),
        ('REC', 'Recursal'),
        ('HOM', 'Homologado'),
        
        # Suspensões
        ('SUS', 'Suspenso'),
        ('AUS', 'Suspenso por Ausência de Partes'),
        ('PER', 'Suspenso por Perícia'),
        
        # Finalizações
        ('ARQ', 'Arquivado'),
        ('BAI', 'Baixado'),
        ('JUL', 'Julgado'),
        ('EXT', 'Extinto'),
        ('CUM', 'Cumprido'),
        ('LIQ', 'Liquidado'),
        
        # Situações Especiais
        ('DES', 'Desmembrado'),
        ('INC', 'Incidente Processual'),
        ('INT', 'Intervenção de Terceiro'),
        ('UNI', 'Unificado'),
    ]
    
    situacao_atual = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        choices=SITUACAO_CHOICES,
        default='CAD',
        verbose_name="Situação Atual"
    )
    ultima_atualizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Atualização"
    )
    usuario = models.ForeignKey(   # adc o usuario quando ele tiver pronto
        'auth.user', 
        on_delete=models.PROTECT,
        related_name='processos',
        verbose_name="Usuário Responsável"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )