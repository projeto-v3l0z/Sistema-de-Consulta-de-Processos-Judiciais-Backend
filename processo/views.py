from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView 
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
#from .adapters import datajud, tjsp, tjrj
from processo.adapters.datajud import buscar_processo_datajud


from .models import Processo
from .filters import ProcessoFilter
from .serializers import ProcessoSerializer

from movimentacao.models import Movimentacao
from movimentacao.serializers import MovimentacaoSerializer

from parte.models import Parte
from parte.serializers import ParteSerializer

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q

from integrations.datajud_adapter import DatajudAdapter
from integrations.tjsp_adapter import TJSPAdapter

# botei pra testar se lembra de mudar os permissoes depois quando tiver usuarios
AUTH_ON = False

# CRUD
from core.ratelimit_preset import Generico
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit



@method_decorator(cache_page(30), name="get")
@method_decorator(ratelimit(key="ip", rate='10/m', block=True), name="get")
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
class MovimentacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = MovimentacaoSerializer
    
    def get_queryset(self):
        get_object_or_404(Processo, pk=self.kwargs['pk'])
        return Movimentacao.objects.filter(processo_id=self.kwargs['pk']).order_by('-data_movimentacao')

    def perform_create(self, serializer):
        processo = get_object_or_404(Processo, pk=self.kwargs['pk'])
        serializer.save(processo=processo)

# Partes
class ParteListCreateView(generics.ListCreateAPIView):
    serializer_class = ParteSerializer

    def get_queryset(self):
        get_object_or_404(Processo, pk=self.kwargs['pk'])
        return Parte.objects.filter(processo_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        processo = get_object_or_404(Processo, pk=self.kwargs['pk'])
        serializer.save(processo=processo)

class ParteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParteSerializer

    def get_queryset(self):
        return Parte.objects.filter(processo_id=self.kwargs['processo_pk'])

class MovimentacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        return Movimentacao.objects.filter(processo_id=self.kwargs['processo_pk'])


    
# Forçar Atualização
class ProcessoForcarAtualizacaoView(APIView):
    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        processo.ultima_atualizacao = timezone.now()
        processo.save()
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Exemplo de views para consulta ao Datajud
class ConsultaDatajudNumeroView(APIView):
    def get(self, request):
        numero = request.query_params.get('numero') # Obtém o número do processo dos parâmetros da requisição
        resultado = DatajudAdapter().consultar_por_numero(numero) 
        return Response(resultado)
    
class ConsultaDatajudDocumentoView(APIView):
    def get(self, request):
        documento = request.query_params.get('documento')  # Obtém o CPF ou CNPJ dos parâmetros da requisição
        resultado = DatajudAdapter().consultar_por_documento(documento)
        return Response(resultado)
    
# Exemplo de views para consulta ao TJSP
class ConsultaTJSPNumeroView(APIView):
    def get(self, request):
        numero = request.query_params.get('numero')  # Obtém o número do processo dos parâmetros da requisição
        resultado = TJSPAdapter().consultar_por_numero(numero)
        return Response(resultado)
    
class ConsultaTJSPDocumentoView(APIView):
    def get(self, request):
        documento = request.query_params.get('documento')  # Obtém o CPF ou CNPJ dos parâmetros da requisição
        resultado = TJSPAdapter().consultar_por_documento(documento)
        return Response(resultado)