from django.contrib import admin
from .models import Processo

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    search_fields = ['numero_processo']
    list_display = ['numero_processo', 'tribunal', 'situacao_atual']




# Register your models here.
