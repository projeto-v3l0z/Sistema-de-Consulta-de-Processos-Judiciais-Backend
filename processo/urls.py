from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListView,
    ParteListView,
    ProcessoBuscaView,
    ProcessoForcarAtualizacaoView,
    ProcessoBuscaDocumentoView
)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    path('<uuid:pk>/', ProcessoRetrieveUpdateDestroyView.as_view(), name='processo-detail'),
    path('<uuid:pk>/movimentacoes/', MovimentacaoListView.as_view(), name='movimentacao-list'),
    path('<uuid:pk>/partes/', ParteListView.as_view(), name='parte-list'),
    path('busca/', ProcessoBuscaView.as_view(), name='processo-busca'),
    path('<uuid:pk>/atualizar/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
    path('busca-documento/', ProcessoBuscaDocumentoView.as_view(), name='processo-busca-documento'),
]