from rest_framework import generics
from .models import Movimentacao
from .serializers import MovimentacaoSerializer

class MovimentacaoListCreateView(generics.ListCreateAPIView):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

class MovimentacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
class MovimentacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = MovimentacaoSerializer
    def get_queryset(self):
        get_object_or_404(Processo, pk=self.kwargs['pk'])
        return Movimentacao.objects.filter(processo_id=self.kwargs['pk']).order_by('-data_movimentacao')
    def perform_create(self, serializer):
        processo = get_object_or_404(Processo, pk=self.kwargs['pk'])
        serializer.save(processo=processo)

class MovimentacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovimentacaoSerializer
    def get_queryset(self):
        return Movimentacao.objects.filter(processo_id=self.kwargs['processo_pk'])