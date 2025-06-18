from rest_framework import serializers
from .models import Parte

class ParteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parte
        fields = '__all__'