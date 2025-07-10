# logs/views.py
from rest_framework import viewsets, permissions
from rest_framework.renderers import JSONRenderer
from django.http import StreamingHttpResponse
import csv
from .models import ConsultaLog
from .serializers import ConsultaLogSerializer

#Pra ativar a permissão de admin, descomente a classe abaixo e a permission_classes na 
# classe ConsultaLogViewSet
# class IsAdmin(permissions.IsAdminUser):
#     pass

class ConsultaLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConsultaLog.objects.select_related('usuario')
    serializer_class = ConsultaLogSerializer
    # permission_classes = [IsAdmin]
    renderer_classes = [JSONRenderer]  # usa JSON normal; CSV via action abaixo

    # GET /api/logs/export_csv/
    def list(self, request, *args, **kwargs):
        if request.query_params.get('format') == 'csv':
            return self._export_csv()
        return super().list(request, *args, **kwargs)

    def _export_csv(self):
        qs = self.get_queryset().values_list(
            'timestamp', 'usuario__username', 'numero_processo', 'metodo', 'endpoint'
        )
        def gen():
            yield ['timestamp', 'usuario', 'numero_processo', 'metodo', 'endpoint']
            for row in qs:
                yield [str(c) if c else '' for c in row]

        response = StreamingHttpResponse(
            (','.join(r)+'\n' for r in gen()),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename=logs.csv'
        return response
