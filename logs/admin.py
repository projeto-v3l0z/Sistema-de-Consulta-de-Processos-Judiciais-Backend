# logs/admin.py
from django.contrib import admin
from .models import ConsultaLog

@admin.register(ConsultaLog)
class ConsultaLogAdmin(admin.ModelAdmin):
    list_display  = ('timestamp', 'usuario', 'numero_processo', 'metodo', 'endpoint')
    search_fields = ('usuario__username', 'numero_processo', 'endpoint')
    list_filter   = ('metodo', 'timestamp')
