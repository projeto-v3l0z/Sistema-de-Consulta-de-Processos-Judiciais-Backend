from django.core.management.base import BaseCommand
from processo.models import Processo
from movimentacao.models import Movimentacao
from parte.models import Parte
from tribunais.models import Tribunal
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Remove todos os dados de teste criados pelo seeder"

    def handle(self, *args, **kwargs):
        Movimentacao.objects.all().delete()
        Parte.objects.all().delete()
        Processo.objects.all().delete()
        Tribunal.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS("Dados de teste removidos."))
