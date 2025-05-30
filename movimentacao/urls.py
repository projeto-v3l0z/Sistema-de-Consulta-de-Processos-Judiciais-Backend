from django.urls import path
from .views import MovimentacaoListCreateView, MovimentacaoRetrieveUpdateDestroyView

urlpatterns = [
    path('movimentacoes/', MovimentacaoListCreateView.as_view(), name='movimentacao-list-create'),
    path('movimentacoes/<uuid:pk>/', MovimentacaoRetrieveUpdateDestroyView.as_view(), name='movimentacao-detail'),
]