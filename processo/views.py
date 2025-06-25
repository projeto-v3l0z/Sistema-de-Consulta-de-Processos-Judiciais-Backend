from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView 
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
#from .adapters import datajud, tjsp, tjrj
from processo.adapters.datajud import buscar_processo_datajud


from .models import Processo
from .filters import ProcessoFilter
from .serializers import ProcessoSerializer, ProcessoBuscaSerializer

from movimentacao.models import Movimentacao
from movimentacao.serializers import MovimentacaoSerializer

from parte.models import Parte
from parte.serializers import ParteSerializer

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q


from .services import buscar_processo_com_fallback

# botei pra testar se lembra de mudar os permissoes depois quando tiver usuarios
AUTH_ON = False

# CRUD

# create & List
class ProcessoListCreateView(generics.ListCreateAPIView):
    queryset = Processo.objects.all().order_by('-created_at')
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProcessoFilter

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
    
# Forçar Atualização
class ProcessoForcarAtualizacaoView(APIView):
    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        processo.ultima_atualizacao = timezone.now()
        processo.save()
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Busca

class BuscaProcessoView(APIView):
    def post(self, request):
        serializer = ProcessoBuscaSerializer(data=request.data)
        if serializer.is_valid():
            numero = serializer.validated_data['numero_processo']
            resultado = buscar_processo_com_fallback(numero)
            if resultado:
                return Response(resultado, status=status.HTTP_200_OK)
            return Response({"detail": "Processo não encontrado em nenhuma fonte."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    