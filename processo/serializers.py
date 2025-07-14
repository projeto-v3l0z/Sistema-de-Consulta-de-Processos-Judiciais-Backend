from rest_framework import serializers
from .models import Processo
from .mapeamentos import CLASSES

class ProcessoSerializer(serializers.ModelSerializer):
    # Caso queira expor a descricao tambem
    situacao_atual_descricao = serializers.SerializerMethodField()
    classe_processual_nome = serializers.SerializerMethodField() # Para retornar o nome da classe processual mapeada

    class Meta:
        model = Processo
        fields = [
            'id',
            'numero_processo',
            'tribunal',
            'classe_processual',
            'classe_processual_nome',
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
    
    def get_classe_processual_nome(self, obj):
        return CLASSES.get(obj.classe_processual, obj.classe_processual) # Retorna o nome mapeado ou o código se não existir no mapeamento