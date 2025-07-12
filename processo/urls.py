from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListView,
    ParteListView,
    BuscaProcessoView,
    ProcessoForcarAtualizacaoView,

    ConsultaDatajudNumeroView,
    ConsultaDatajudDocumentoView,
    ConsultaTJSPNumeroView,
    ConsultaTJSPDocumentoView,

)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    
    path('<uuid:pk>/movimentacoes/', MovimentacaoListView.as_view(), name='movimentacao-list'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
    path('<uuid:pk>/partes/', ParteListView.as_view(), name='parte-list'),
    
    path('busca/', ProcessoBuscaView.as_view(), name='processo-busca'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
    
    path('consulta-datajud/numero/', ConsultaDatajudNumeroView.as_view(), name='consulta-datajud-numero'), # Exemplos de views para consulta ao adaptador Datajud
    path('consulta-datajud/documento/', ConsultaDatajudDocumentoView.as_view(), name='consulta-datajud-documento'),
    path('consulta-tjsp/numero/', ConsultaTJSPNumeroView.as_view(), name='consulta-tjsp-numero'),  # Exemplos de views para consulta ao adaptador TJSP
    path('consulta-tjsp/documento/', ConsultaTJSPDocumentoView.as_view(), name='consulta-tjsp-documento'),
]

# busca_processo