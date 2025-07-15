from rest_framework import serializers
from .models import Movimentacao

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'processo',
            'data_movimentacao',
            'tipo_movimentacao',
            'descricao',
            'responsavel',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'processo', 'created_at', 'updated_at']

class StandardMovimentacaoSerializer(serializers.Serializer):
    data_movimentacao = serializers.DateTimeField()
    descricao         = serializers.CharField()