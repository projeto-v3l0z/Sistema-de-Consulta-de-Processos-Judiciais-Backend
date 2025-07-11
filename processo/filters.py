# processo/filters.py
import django_filters as df
from .models import Processo

class ProcessoFilter(df.FilterSet):
    tribunal = df.CharFilter(field_name="tribunal", lookup_expr="iexact")
    classe  = df.CharFilter(field_name="classe_processual", lookup_expr="iexact")

    # opcionais
    grau         = df.CharFilter(field_name="grau", lookup_expr="iexact")
    nivelSigilo  = df.CharFilter(field_name="nivel_sigilo", lookup_expr="iexact")
    formato      = df.CharFilter(field_name="formato", lookup_expr="iexact")
    sistema      = df.CharFilter(field_name="sistema", lookup_expr="iexact")

    class Meta:
        model  = Processo
        fields = ["tribunal", "classe", "grau", "nivelSigilo", "formato", "sistema"]
