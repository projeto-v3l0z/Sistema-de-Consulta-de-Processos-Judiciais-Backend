from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re
from .models import Processo
from .filters import ProcessoFilter
from .serializers import (
    ProcessoSerializer,
    StandardProcessoSerializer,
    StandardParteSerializer,
    StandardMovimentacaoSerializer,
)
from .services import (
    consultar_processos_por_documento,
    get_processo,
)
from movimentacao.models import Movimentacao
from movimentacao.serializers import MovimentacaoSerializer
from parte.models import Parte
from parte.serializers import ParteSerializer

from integrations.datajud_adapter import DatajudAdapter
from integrations.tjsp_adapter import TJSPAdapter

AUTH_ON = False

# List & Create com serialização padrão customizada
class ProcessoListCreateView(generics.ListCreateAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProcessoFilter

    def get_queryset(self):
        qs = super().get_queryset()
        tribunal = self.request.query_params.get('tribunal')
        numero = self.request.query_params.get('numero')
        situacao = self.request.query_params.get('situacao')
        if tribunal:
            qs = qs.filter(tribunal=tribunal)
        if numero:
            qs = qs.filter(numero_processo__icontains=numero)
        if situacao:
            qs = qs.filter(situacao_atual=situacao)
        return qs.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                "numero_processo":   p.numero_processo,
                "tribunal":          p.tribunal,
                "classe_processual": p.classe_processual,
                "assunto":           p.assunto,
                "data_distribuicao": p.data_distribuicao,
                "orgao_julgador":    p.orgao_julgador,
                "situacao_atual":    p.situacao_atual,
            }
            for p in queryset
        ]
        serializer = StandardProcessoSerializer(data, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        inst = self.get_queryset().get(pk=resp.data['id'])
        data = {
            "numero_processo":   inst.numero_processo,
            "tribunal":          inst.tribunal,
            "classe_processual": inst.classe_processual,
            "assunto":           inst.assunto,
            "data_distribuicao": inst.data_distribuicao,
            "orgao_julgador":    inst.orgao_julgador,
            "situacao_atual":    inst.situacao_atual,
        }
        serializer = StandardProcessoSerializer(data)
        return Response(serializer.data, status=resp.status_code)

# Retrieve/Update/Delete com serialização padrão customizada
class ProcessoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())

    def retrieve(self, request, *args, **kwargs):
        inst = self.get_object()
        data = {
            "numero_processo":   inst.numero_processo,
            "tribunal":          inst.tribunal,
            "classe_processual": inst.classe_processual,
            "assunto":           inst.assunto,
            "data_distribuicao": inst.data_distribuicao,
            "orgao_julgador":    inst.orgao_julgador,
            "situacao_atual":    inst.situacao_atual,
        }
        serializer = StandardProcessoSerializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        resp = super().update(request, *args, **kwargs)
        inst = self.get_object()
        data = {
            "numero_processo":   inst.numero_processo,
            "tribunal":          inst.tribunal,
            "classe_processual": inst.classe_processual,
            "assunto":           inst.assunto,
            "data_distribuicao": inst.data_distribuicao,
            "orgao_julgador":    inst.orgao_julgador,
            "situacao_atual":    inst.situacao_atual,
        }
        serializer = StandardProcessoSerializer(data)
        return Response(serializer.data, status=resp.status_code)

# Movimentações
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

# Partes
class ParteListView(generics.ListAPIView):
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

# Forçar Atualização
class ProcessoForcarAtualizacaoView(APIView):
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        processo.ultima_atualizacao = timezone.now()
        processo.save()
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Busca por número de processo (com fallback)
class BuscaProcessoView(APIView):
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    def post(self, request):
        serializer = ProcessoBuscaSerializer(data=request.data)
        if serializer.is_valid():
            numero = serializer.validated_data['numero_processo']
            resultado = buscar_processo_com_fallback(numero)
            if resultado:
                return Response(resultado, status=status.HTTP_200_OK)
            return Response({"detail": "Processo não encontrado em nenhuma fonte."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Busca por termo (número ou documento)
class ProcessoBuscaView(APIView):
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'termo': openapi.Schema(type=openapi.TYPE_STRING)}
    ))
    def post(self, request):
        termo = request.data.get('termo', '').strip()
        if not termo:
            return Response({'detail': 'Informe um termo.'}, status=400)
        qs = Processo.objects.filter(
            Q(numero_processo__icontains=termo) |
            Q(partes__documento__icontains=termo)
        ).distinct()
        data = [
            {
                "numero_processo":   p.numero_processo,
                "tribunal":          p.tribunal,
                "classe_processual": p.classe_processual,
                "assunto":           p.assunto,
                "data_distribuicao": p.data_distribuicao,
                "orgao_julgador":    p.orgao_julgador,
                "situacao_atual":    p.situacao_atual,
            }
            for p in qs
        ]
        serializer = StandardProcessoSerializer(data, many=True)
        return Response(serializer.data)

# Busca por documento (CPF/CNPJ)
class ProcessoBuscaDocumentoView(APIView):
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'documento': openapi.Schema(type=openapi.TYPE_STRING)}
    ))
    def post(self, request):
        documento = request.data.get('documento', '').strip()
        if not re.fullmatch(r'\d{11}|\d{14}', documento):
            return Response(
                {'error': 'Documento inválido. Informe um CPF (11 dígitos) ou CNPJ (14 dígitos).'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            fonte = request.query_params.get('fonte')
            if fonte:
                dtos = consultar_processos_por_documento(documento, fonte)
            else:
                from .services import ADAPTERS
                dtos = []
                for key, adapter in ADAPTERS.items():
                    try:
                        dtos.extend(adapter.consultar_por_documento(documento))
                    except Exception:
                        continue
            data = [
                {
                    "numero_processo":   dto.numero_processo,
                    "tribunal":          dto.tribunal,
                    "classe_processual": dto.classe_processual,
                    "assunto":           dto.assunto,
                    "data_distribuicao": dto.data_distribuicao,
                    "orgao_julgador":    dto.orgao_julgador,
                    "situacao_atual":    dto.situacao_atual,
                }
                for dto in dtos
            ]
            serializer = StandardProcessoSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {'error': 'Erro interno ao consultar processos por documento.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Integrações externas
class ConsultaDatajudNumeroView(APIView):
    def get(self, request):
        numero = request.query_params.get('numero')
        resultado = DatajudAdapter().consultar_por_numero(numero)
        return Response(resultado)

class ConsultaDatajudDocumentoView(APIView):
    def get(self, request):
        documento = request.query_params.get('documento')
        resultado = DatajudAdapter().consultar_por_documento(documento)
        return Response(resultado)

class ConsultaTJSPNumeroView(APIView):
    def get(self, request):
        numero = request.query_params.get('numero')
        resultado = TJSPAdapter().consultar_por_numero(numero)
        return Response(resultado)

class ConsultaTJSPDocumentoView(APIView):
    def get(self, request):
        documento = request.query_params.get('documento')
        resultado = TJSPAdapter().consultar_por_documento(documento)
        return Response(resultado)