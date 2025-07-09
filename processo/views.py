from rest_framework import generics, status
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

import re

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Processo
from .serializers import (ProcessoSerializer, StandardProcessoSerializer, StandardParteSerializer, StandardMovimentacaoSerializer)
from .services import get_processo, consultar_processos_por_documento # <-- nossos servições de adaptadores

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
# create & List
@method_decorator(cache_page(30), name="get")
@method_decorator(ratelimit(key="ip", rate='10/m', block=True), name="get")
class ProcessoListCreateView(generics.ListCreateAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

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


    #Para padronizar a resposta de criação:
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



class MovimentacaoListView(generics.ListAPIView):
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Movimentacao.objects.none()
        return Movimentacao.objects.filter(processo_id=self.kwargs['pk']).order_by('-data_movimentacao')

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = [
            {
                "data_movimentacao": mv.data_movimentacao,
                "descricao":         mv.descricao,
            }
            for mv in qs
        ]
        serializer = StandardMovimentacaoSerializer(data, many=True)
        return Response(serializer.data)



class ParteListView(generics.ListAPIView):
    """
    Lista as partes de um processo.
    Escapa do schema-gen quando swagger_fake_view=True.
    """
    def list(self, request, *args, **kwargs):
        # Pega o queryset normalmente (já respeita swagger_fake_view)
        qs = self.get_queryset()
        # Monta o JSON só com os campos padronizados
        data = [
            {
                "nome":      parte.nome,
                "documento": parte.documento,
            }
            for parte in qs
        ]
        serializer = StandardParteSerializer(data, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # mantém o escape para o Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Parte.objects.none()
        return Parte.objects.filter(processo_id=self.kwargs['pk'])


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


class ProcessoForcarAtualizacaoView(APIView):
    """
    Chama o adaptador externo, padroniza e atualiza o Processo no banco.
    """
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

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
    

#Views da renderização
class ProcessoListViewHTML(ListView):
    model = Processo
    template_name = 'processo/listProcessoView.html'    
    context_object_name = 'processo'         
    paginate_by = 20                         
    ordering = ['-created_at'] 