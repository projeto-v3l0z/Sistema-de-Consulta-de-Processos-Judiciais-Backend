from rest_framework import serializers
from .models import Processo

class ProcessoSerializer(serializers.ModelSerializer):
    # Caso queira expor a descricao tambem
    situacao_atual_descricao = serializers.SerializerMethodField()

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
            'situacao_atual_descricao',  
            'ultima_atualizacao',
        ]

    def get_situacao_atual_descricao(self, obj):
        return obj.get_situacao_atual_display()


class StandardProcessoSerializer(serializers.Serializer):
    numero_processo   = serializers.CharField()
    tribunal          = serializers.CharField()
    classe_processual = serializers.CharField()
    assunto           = serializers.CharField()
    data_distribuicao = serializers.DateField()
    orgao_julgador    = serializers.CharField()
    situacao_atual    = serializers.CharField()

# Isso é para a classe de movimentações na views
class StandardMovimentacaoSerializer(serializers.Serializer):
    data_movimentacao = serializers.DateTimeField()
    descricao         = serializers.CharField()

# Isso é para a classe de Partes
class StandardParteSerializer(serializers.Serializer):
    nome      = serializers.CharField()
    documento = serializers.CharField()