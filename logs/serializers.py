# logs/serializers.py
from rest_framework import serializers
from .models import ConsultaLog

class ConsultaLogSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = ConsultaLog
        fields = '__all__'
