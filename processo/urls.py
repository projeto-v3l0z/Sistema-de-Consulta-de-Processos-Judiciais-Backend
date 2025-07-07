from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListCreateView,
    ParteListCreateView,
    BuscaProcessoView,
    ProcessoForcarAtualizacaoView,
    ParteRetrieveUpdateDestroyView,
    MovimentacaoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    path('<uuid:pk>/', ProcessoRetrieveUpdateDestroyView.as_view(), name='processo-detail'),
    path('<uuid:pk>/movimentacoes/', MovimentacaoListCreateView.as_view(), name='processo-movimentacao-list'),
    path('<uuid:processo_pk>/movimentacoes/<uuid:pk>/', MovimentacaoRetrieveUpdateDestroyView.as_view(), name='processo-movimentacao-detail'),
    path('<uuid:pk>/partes/', ParteListCreateView.as_view(), name='processo-parte-list'),
    path('<uuid:processo_pk>/partes/<uuid:pk>/', ParteRetrieveUpdateDestroyView.as_view(), name='processo-parte-detail'),
    path('buscar/', BuscaProcessoView.as_view(), name='busca-processo'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
]

# busca_processo