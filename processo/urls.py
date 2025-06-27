# processos/urls.py
from django.urls import path
from .views import (
    ProcessoListCreateView,
    ProcessoRetrieveUpdateDestroyView,
    MovimentacaoListView,
    ParteListView,
    ProcessoBuscaView,
    ProcessoForcarAtualizacaoView,
)

urlpatterns = [
    path('', ProcessoListCreateView.as_view(), name='processo-list'),
    path('<uuid:pk>/', ProcessoRetrieveUpdateDestroyView.as_view(), name='processo-detail'),
    path('<uuid:pk>/movimentacoes/', MovimentacaoListView.as_view(), name='movimentacao-list'),
    path('<uuid:pk>/partes/', ParteListView.as_view(), name='parte-list'),
    path('busca/', ProcessoBuscaView.as_view(), name='processo-busca'),
    path('<uuid:pk>/atualizar-externo/', ProcessoForcarAtualizacaoView.as_view(), name='processo-forcar-atualizacao'),
]
