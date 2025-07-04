# isso define como vai ser o formato padrão
from dataclasses import dataclass
from rest_framework import serializers

@dataclass
class ProcessoDTO:
    numero_processo: str
    tribunal: str
    classe_processual: str
    assunto: str
    data_distribuicao: str   
    orgao_julgador: str
    situacao_atual: str

#isso não é ligador ao model, isso é para garantir que todas as views internas devolvem o mesmo formato do json
class StandardProcessoSerializer(serializers.Serializer):
    numero_processo   = serializers.CharField()
    tribunal          = serializers.CharField()
    classe_processual = serializers.CharField()
    assunto           = serializers.CharField()
    data_distribuicao = serializers.DateField()
    orgao_julgador    = serializers.CharField()
    situacao_atual    = serializers.CharField()

