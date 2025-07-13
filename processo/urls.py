from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListCreateView,
    MovimentacaoRetrieveUpdateDestroyView,
    ParteListCreateView,
    ParteRetrieveUpdateDestroyView,
    ProcessoForcarAtualizacaoView,
    BuscaProcessoView,
    ProcessoBuscaView,
    ProcessoBuscaDocumentoView,
    ConsultaDatajudNumeroView,
    ConsultaDatajudDocumentoView,
    ConsultaTJSPNumeroView,
    ConsultaTJSPDocumentoView,
)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    path('<uuid:pk>/', ProcessoRetrieveUpdateDestroyView.as_view(), name='processo-detail'),

    # Movimentações
    path('<uuid:pk>/movimentacoes/', MovimentacaoListCreateView.as_view(), name='movimentacao-list'),
    path('<uuid:processo_pk>/movimentacoes/<uuid:pk>/', MovimentacaoRetrieveUpdateDestroyView.as_view(), name='processo-movimentacao-detail'),

    # Partes
    path('<uuid:pk>/partes/', ParteListCreateView.as_view(), name='processo-parte-list'),
    path('<uuid:processo_pk>/partes/<uuid:pk>/', ParteRetrieveUpdateDestroyView.as_view(), name='processo-parte-detail'),

    # Forçar atualização
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),

    # Buscas
    path('busca/', BuscaProcessoView.as_view(), name='processo-busca'),
    path('busca-numero/', ProcessoBuscaView.as_view(), name='processo-busca-numero'),
    path('busca-documento/', ProcessoBuscaDocumentoView.as_view(), name='processo-busca-documento'),

    # Integrações externas
    path('consulta-datajud/numero/', ConsultaDatajudNumeroView.as_view(), name='consulta-datajud-numero'),
    path('consulta-datajud/documento/', ConsultaDatajudDocumentoView.as_view(), name='consulta-datajud-documento'),
    path('consulta-tjsp/numero/', ConsultaTJSPNumeroView.as_view(), name='consulta-tjsp-numero'),
    path('consulta-tjsp/documento/', ConsultaTJSPDocumentoView.as_view(), name='consulta-tjsp-documento'),
]