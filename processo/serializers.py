from rest_framework import serializers
from .models import Processo, Movimentacao

class ProcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processo
        fields = [
            'id',
            'numero_processo',
            'tribunal',
            'classe_processual',
            'assunto',
            'data_distribuicao',
            'orgao_julgador',
            'valor_causa',
            'situacao_atual',
            'ultima_atualizacao',
            'usuario'
        ] 

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'processo',
            'data',
            'descricao',
            'observacao',
        ]