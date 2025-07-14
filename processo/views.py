from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import Processo
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

from django.db import connections
from django.db.utils import OperationalError
import redis
from django.core.cache import cache

from .mapeamentos import CLASSES, MOVIMENTOS, FORMATOS

# botei pra testar se lembra de mudar os permissoes depois quando tiver usuarios
AUTH_ON = False

# CRUD
from core.ratelimit_preset import Generico
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit

# create & List
@method_decorator(cache_page(30), name="get")
@method_decorator(ratelimit(key="ip", rate='10/m', block=True), name="get")
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
    

class HealthCheckView(APIView):
    def get(self, request):
        health = {}

        # PostgreSQL
        try:
            connections['default'].cursor() # Testa a conexão com o banco de dados
            health['postgresql'] = 'ok'
        except OperationalError: # OperationalError é lançado se a conexão falhar
            health['postgresql'] = 'unavailable'

        # Redis
        try:
            r = redis.Redis.from_url('redis://redis:6379/0')
            r.ping()
            health['redis'] = 'ok'
        except Exception:
            health['redis'] = 'unavailable'

        # Cache
        try:
            cache.set('health_check', 'ok', timeout=5) # Define um valor no cache para testar
            value = cache.get('health_check')
            health['cache'] = 'ok' if value == 'ok' else 'unavailable' # Verifica se o valor no cache é o esperado
        except Exception:
            health['cache'] = 'unavailable'

        # Retorna 200 se tudo estiver ok, 503 se algum serviço estiver indisponível
        return Response(health, status=status.HTTP_200_OK if all(v == 'ok' for v in health.values()) else status.HTTP_503_SERVICE_UNAVAILABLE) 

class ProcessoMovimentosPagination(LimitOffsetPagination): # Controla quantidade de resultados por página
    default_limit = 20
    max_limit = 100

class ProcessoMovimentosView(APIView):
    def get(self, request, numero):
        processo = get_object_or_404(Processo, numero_processo=numero)
        movimentos_qs = Movimentacao.objects.filter(processo=processo).order_by('-data_movimentacao')
        paginator = ProcessoMovimentosPagination()
        result_page = paginator.paginate_queryset(movimentos_qs, request)
        movimentos = []
        for mov in result_page:
            movimentos.append({
                "dataHora": mov.data_movimentacao,
                #"nome": MOVIMENTOS.get(mov.codigo, mov.nome or 'Movimento não identificado'),
                #"codigo": mov.codigo,
                #"complementosTabelados": getattr(mov, 'complementos_tabelados', []) or []
            })
        return paginator.get_paginated_response(movimentos)


class MapeamentosView(APIView):
    # Endpoint para retornar os mapeamentos de classes, movimentos e formatos
    def get(self, request):
        return Response({
            'classes': CLASSES,
            'movimentos': MOVIMENTOS,
            'formatos': FORMATOS
        })