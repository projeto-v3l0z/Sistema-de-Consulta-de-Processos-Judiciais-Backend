from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListCreateView,
    ParteListCreateView,
    ProcessoForcarAtualizacaoView,
    ParteRetrieveUpdateDestroyView,
    MovimentacaoRetrieveUpdateDestroyView,

    ConsultaDatajudNumeroView,
    ConsultaDatajudDocumentoView,
    ConsultaTJSPNumeroView,
    ConsultaTJSPDocumentoView,

)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    
    path('<uuid:pk>/movimentacoes/', MovimentacaoListCreateView.as_view(), name='processo-movimentacao-list'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
    path('<uuid:processo_pk>/movimentacoes/<uuid:pk>/', MovimentacaoRetrieveUpdateDestroyView.as_view(), name='processo-movimentacao-detail'),
    path('<uuid:pk>/partes/', ParteListCreateView.as_view(), name='processo-parte-list'),
    path('<uuid:processo_pk>/partes/<uuid:pk>/', ParteRetrieveUpdateDestroyView.as_view(), name='processo-parte-detail'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
    path('consulta-datajud/numero/', ConsultaDatajudNumeroView.as_view(), name='consulta-datajud-numero'), 
    path('consulta-datajud/documento/', ConsultaDatajudDocumentoView.as_view(), name='consulta-datajud-documento'),
    path('consulta-tjsp/numero/', ConsultaTJSPNumeroView.as_view(), name='consulta-tjsp-numero'),  
    path('consulta-tjsp/documento/', ConsultaTJSPDocumentoView.as_view(), name='consulta-tjsp-documento'),
]

# busca_processo