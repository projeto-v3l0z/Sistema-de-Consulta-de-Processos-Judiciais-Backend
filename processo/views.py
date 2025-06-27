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
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Processo
from .serializers import ProcessoSerializer
from .services import get_processo  # <-- nossos servições de adaptadores

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


class ProcessoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Processo.objects.all()
    serializer_class = ProcessoSerializer
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())


class MovimentacaoListView(generics.ListAPIView):
    """
    Lista as movimentações de um processo.
    Escapa do schema-gen quando swagger_fake_view=True.
    """
    serializer_class = MovimentacaoSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Movimentacao.objects.none()
        return Movimentacao.objects.filter(processo_id=self.kwargs['pk']) \
                                  .order_by('-data_movimentacao')


class ParteListView(generics.ListAPIView):
    """
    Lista as partes de um processo.
    Escapa do schema-gen quando swagger_fake_view=True.
    """
    serializer_class = ParteSerializer

    def get_queryset(self):
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
            return Response(
                {'detail': 'Informe um termo de busca.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = Processo.objects.filter(
            Q(numero_processo__icontains=termo) |
            Q(partes__documento__icontains=termo)
        ).distinct()
        serializer = ProcessoSerializer(qs, many=True)
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
            # Atualiza campos padronizados
            processo.tribunal           = dto.tribunal
            processo.classe_processual  = dto.classe_processual
            processo.assunto            = dto.assunto
            processo.data_distribuicao  = dto.data_distribuicao
            processo.orgao_julgador     = dto.orgao_julgador
            processo.situacao_atual     = dto.situacao_atual
            processo.ultima_atualizacao = timezone.now()
            processo.save()

            serializer = ProcessoSerializer(processo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )