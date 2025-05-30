from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Processo, Movimentacao
from .serializers import ProcessoSerializer, MovimentacaoSerializer
from django.utils import timezone


# botei pra testar se lembra de mudar os permissoes depois quando tiver usuarios
AUTH_ON = False

# CRUD

# create & List
class ProcessoListCreateView(generics.ListCreateAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Processo.objects.all()  # Processo.objects.filter(usuario=self.request.user)
        tribunal = self.request.query_params.get('tribunal', None)
        numero = self.request.query_params.get('numero', None)
        situacao = self.request.query_params.get('situacao', None)
        if tribunal:
            queryset = queryset.filter(tribunal=tribunal)
        if numero:
            queryset = queryset.filter(numero_processo__icontains=numero)
        if situacao:
            queryset = queryset.filter(situacao_atual=situacao)
        return queryset.order_by('-created_at')

# Read & Update & Delete
class ProcessoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    
    def get_queryset(self):
        return Processo.objects.all()  # Processo.objects.filter(usuario=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())

# movimentacao
class MovimentacaoListView(generics.ListAPIView):
    serializer_class = MovimentacaoSerializer
    
    def get_queryset(self):
        processo_id = self.kwargs['pk']
        return Movimentacao.objects.filter(processo_id=processo_id).order_by('-data')