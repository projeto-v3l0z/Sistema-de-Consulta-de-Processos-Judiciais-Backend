from django.contrib import admin
from .models import Tribunal

@admin.register(Tribunal)
class TribunalAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'estado', 'api_tipo', 'updated_at')
    search_fields = ('sigla', 'nome', 'estado')
