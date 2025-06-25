import django_filters
from .models import Processo

class ProcessoFilter(django_filters.FilterSet):
    numero_processo = django_filters.CharFilter(field_name='numero_processo', lookup_expr='icontains')
    tribunal = django_filters.CharFilter(field_name='tribunal', lookup_expr='icontains')
    classe_processual = django_filters.CharFilter(field_name='classe_processual', lookup_expr='icontains')
    orgao_julgador = django_filters.CharFilter(field_name='orgao_julgador', lookup_expr='icontains')
    situacao_atual = django_filters.CharFilter(field_name='situacao_atual', lookup_expr='exact')
    usuario = django_filters.CharFilter(field_name='usuario__username', lookup_expr='icontains')
    
    class Meta:
        model = Processo
        fields = ['numero_processo', 'tribunal', 'classe_processual', 'orgao_julgador', 'situacao_atual', 'usuario']
    