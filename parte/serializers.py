from rest_framework import serializers
from .models import Parte

class ParteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parte
        fields = [
            'id',
            'processo',
            'nome',
            'tipo_parte',
            'documento',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'processo', 'created_at', 'updated_at']
class StandardParteSerializer(serializers.Serializer):
    nome      = serializers.CharField()
    documento = serializers.CharField()