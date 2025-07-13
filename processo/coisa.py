from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

import re  # ← NOVO: para validar CPF/CNPJ

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Processo
from .serializers import (
    ProcessoSerializer,
    StandardProcessoSerializer,
    StandardParteSerializer,
)
from .services import (
    get_processo,
    consultar_processos_por_documento,  # ← IMPORTADO o novo serviço
)

from movimentacao.models import Movimentacao
from movimentacao.serializers import MovimentacaoSerializer
from parte.models import Parte
from parte.serializers import ParteSerializer

AUTH_ON = False  # Carlos lembrar pfvr de muda pra True quando tiver em produção


class ProcessoListCreateView(generics.ListCreateAPIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


class ProcessoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


class MovimentacaoListView(generics.ListAPIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


class ParteListView(generics.ListAPIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


class ProcessoBuscaView(APIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


class ProcessoForcarAtualizacaoView(APIView):
    ...
    # mantém exatamente o seu código já padronizado
    ...


# =================== NOVA VIEW: Busca por documento ===================

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
        # 1) Validação básica de CPF (11 dígitos) ou CNPJ (14 dígitos)
        if not re.fullmatch(r'\d{11}|\d{14}', documento):
            return Response(
                {'error': 'Documento inválido. Informe um CPF (11 dígitos) ou CNPJ (14 dígitos).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Chama o serviço que delega ao adaptador correto
        try:
            # se quiser especificar fonte: ?fonte=datajud|tjsp|trj, poderia ser argumento
            dtos = consultar_processos_por_documento(documento, fonte=request.query_params.get('fonte', None))
            # 3) Serializa o resultado padronizado
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
