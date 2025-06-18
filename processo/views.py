from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Processo
from .serializers import ProcessoSerializer

from movimentacao.models import Movimentacao
from movimentacao.serializers import MovimentacaoSerializer

from parte.models import Parte
from parte.serializers import ParteSerializer

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q


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
        return Movimentacao.objects.filter(processo_id=processo_id).order_by('-data_movimentacao')

# Partes
class ParteListView(generics.ListAPIView):
    serializer_class = ParteSerializer

    def get_queryset(self):
        processo_id = self.kwargs['pk']
        return Parte.objects.filter(processo_id=processo_id)

# Busca
class ProcessoBuscaView(APIView):
    def post(self, request):
        termo = request.data.get('termo', '').strip()
        if not termo:
            return Response({'detail': 'Informe um termo de busca.'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Processo.objects.filter(
            Q(numero_processo__icontains=termo) |
            Q(partes__documento__icontains=termo)
        ).distinct()
        serializer = ProcessoSerializer(queryset, many=True)
        return Response(serializer.data)

# Forçar Atualização
class ProcessoForcarAtualizacaoView(APIView):
    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        processo.ultima_atualizacao = timezone.now()
        processo.save()
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)