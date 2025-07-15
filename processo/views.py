from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Processo
from .filters import ProcessoFilter
from .serializers import ProcessoSerializer, StandardProcessoSerializer
from integrations.datajud_adapter import DatajudAdapter

AUTH_ON = False

# CRUD de processos
class ProcessoListCreateView(generics.ListCreateAPIView):
    queryset = Processo.objects.all().order_by('-created_at')
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
                "parte_nome":        p.parte_nome,
                "parte_cpf":         p.parte_cpf,
                "valor_causa":       p.valor_causa,
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
            "parte_nome":        p.parte_nome,
            "parte_cpf":         p.parte_cpf,
            "valor_causa":       p.valor_causa,
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
            "parte_nome":        p.parte_nome,
            "parte_cpf":         p.parte_cpf,
            "valor_causa":       p.valor_causa,
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
            "parte_nome":        p.parte_nome,
            "parte_cpf":         p.parte_cpf,
            "valor_causa":       p.valor_causa,
        }
        serializer = StandardProcessoSerializer(data)
        return Response(serializer.data, status=resp.status_code)

# Forçar atualização manual do processo
class ProcessoForcarAtualizacaoView(APIView):
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]
    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        processo.ultima_atualizacao = timezone.now()
        processo.save()
        serializer = ProcessoSerializer(processo)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Pesquisa unificada: banco local + DataJud
class PesquisaUnificadaProcessoView(APIView):
    """
    GET /processos/pesquisa/?numero=...
    Busca no banco local e, se DataJud retornar algo, retorna o resultado do DataJud.
    Se DataJud não retornar nada, retorna apenas o que está no banco (ou vazio).
    """
    permission_classes = [AllowAny] if not AUTH_ON else [IsAuthenticated]

    def get(self, request):
        numero = request.query_params.get("numero")
        if not numero:
            return Response({"erro": "Informe o número do processo."}, status=400)

        # Busca no banco local
        processos = Processo.objects.filter(numero_processo=numero)
        data_local = [
            {
                "numero_processo":   p.numero_processo,
                "tribunal":          p.tribunal,
                "classe_processual": p.classe_processual,
                "assunto":           p.assunto,\
                "data_distribuicao": p.data_distribuicao,
                "orgao_julgador":    p.orgao_julgador,
                "situacao_atual":    p.situacao_atual,
                "parte_nome":        p.parte_nome,
                "parte_cpf":         p.parte_cpf,
                "valor_causa":       p.valor_causa,
            }
            for p in processos
        ]

        # Busca no DataJud
        try:
            adapter = DatajudAdapter()
            datajud_result = adapter.consultar_por_numero(numero)
        except Exception:
            datajud_result = None

        # Se DataJud retornar algo, retorna só ele; senão, retorna o banco local
        if datajud_result:
            serializer = StandardProcessoSerializer(datajud_result, many=isinstance(datajud_result, list))
            return Response(serializer.data)
        else:
            serializer = StandardProcessoSerializer(data_local, many=True)
            return Response(serializer.data)