from django.core.management.base import BaseCommand
from apps.datajud_client.services import consultar_processo

class Command(BaseCommand):
    help = "Testa consulta no Datajud"

    def add_arguments(self, parser):
        parser.add_argument('numero_processo', type=str, help='Número do processo para consulta')

    def handle(self, *args, **options):
        numero = options['numero_processo']
        result = consultar_processo(numero)
        self.stdout.write(self.style.SUCCESS(str(result)))
