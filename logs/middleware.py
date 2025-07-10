# logs/middleware.py
import re
from django.utils.deprecation import MiddlewareMixin
from .models import ConsultaLog

PROCESSO_RE = re.compile(r'/api/processos/(?P<num>\d+)/')
IGNORED = ['/api/logs/']

class AuditoriaMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        if path.startswith(tuple(IGNORED)) or request.method != 'GET':
            return None

        match = PROCESSO_RE.search(path)
        numero_processo = match.group('num') if match else ''

        ConsultaLog.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            numero_processo=numero_processo,
            metodo=request.method,
            endpoint=path
        )
        return None
