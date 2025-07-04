from rest_framework import generics, status
from rest_framework.views import APIView
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

AUTH_ON = False  # Carlos lembrar pfvr de muda pra True quando tiver em produção


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
        fonte = request.query_params.get('fonte')
        if fonte not in ('datajud', 'tjsp', 'trj'):
            return Response(
                {'error': 'fonte inválida. Use datajud, tjsp ou trj.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            dto = get_processo(processo.numero_processo, fonte)
            
            processo.tribunal           = dto.tribunal
            processo.classe_processual  = dto.classe_processual
            processo.assunto            = dto.assunto
            processo.data_distribuicao  = dto.data_distribuicao
            processo.orgao_julgador     = dto.orgao_julgador
            processo.situacao_atual     = dto.situacao_atual
            processo.ultima_atualizacao = timezone.now()
            processo.save()

            data = {
                "numero_processo":   processo.numero_processo,
                "tribunal":          processo.tribunal,
                "classe_processual": processo.classe_processual,
                "assunto":           processo.assunto,
                "data_distribuicao": processo.data_distribuicao,
                "orgao_julgador":    processo.orgao_julgador,
                "situacao_atual":    processo.situacao_atual,
            }
            serializer = StandardProcessoSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class ProcessoBuscaDocumentoView(APIView):
    """
    Busca processos pelo CPF ou CNPJ de uma parte.
    """
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'documento': openapi.Schema(type=openapi.TYPE_STRING)}
    ))
    def post(self, request):
        documento = request.data.get('documento', '').strip()
        # Validação básica de CPF (11 dígitos) ou CNPJ (14 dígitos)
        if not re.fullmatch(r'\d{11}|\d{14}', documento):
            return Response(
                {'error': 'Documento inválido. Informe um CPF (11 dígitos) ou CNPJ (14 dígitos).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chama o serviço que delega ao adaptador correto
        try:
            
            fonte = request.query_params.get('fonte')
            if fonte:
                dtos = consultar_processos_por_documento(documento, fonte)
            else:
                # se não passou fonte, consulta em todas
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
            # Fonte inválida ou outro erro previsível
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # Qualquer outra falha (timeout, parse, etc)
            return Response(
                {'error': 'Erro interno ao consultar processos por documento.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
