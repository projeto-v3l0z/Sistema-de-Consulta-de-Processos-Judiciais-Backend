from rest_framework import serializers
from .models import Processo
import re

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


class ProcessoBuscaSerializer(serializers.Serializer):
    numero_processo = serializers.CharField()

    def validate_numero_processo(self, value):
        pattern = r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Número de processo inválido.")
        return value
