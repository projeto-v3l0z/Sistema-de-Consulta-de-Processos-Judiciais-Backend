from rest_framework import serializers
from .models import Processo

class ProcessoSerializer(serializers.ModelSerializer):
    # Caso queira expor a descricao tambem
    situacao_atual_descricao = serializers.SerializerMethodField()
    parte_nome = serializers.SerializerMethodField()
    parte_cpf = serializers.SerializerMethodField()

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
            'parte_nome',
            'parte_cpf',
            'valor_causa',
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
    parte_nome        = serializers.CharField()
    parte_cpf         = serializers.CharField()
    valor_causa       = serializers.CharField()
