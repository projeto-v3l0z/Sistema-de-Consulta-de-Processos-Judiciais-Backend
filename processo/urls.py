from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,   # se for usar em outra rota
    MovimentacaoListView,
    ParteListView,
    ProcessoBuscaView,
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
    path('consulta-datajud/numero/', ConsultaDatajudNumeroView.as_view(), name='consulta-datajud-numero'),
    path('consulta-datajud/documento/', ConsultaDatajudDocumentoView.as_view(), name='consulta-datajud-documento'),
    path('consulta-tjsp/numero/', ConsultaTJSPNumeroView.as_view(), name='consulta-tjsp-numero'),
    path('consulta-tjsp/documento/', ConsultaTJSPDocumentoView.as_view(), name='consulta-tjsp-documento'),
]
