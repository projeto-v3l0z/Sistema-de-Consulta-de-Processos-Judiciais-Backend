from rest_framework import generics
from .models import Movimentacao
from .serializers import MovimentacaoSerializer

class MovimentacaoListCreateView(generics.ListCreateAPIView):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

class MovimentacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
