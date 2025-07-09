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