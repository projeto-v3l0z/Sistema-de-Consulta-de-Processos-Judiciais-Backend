# apps/datajud_client/management/commands/datajud_test.py

import json
from django.core.management.base import BaseCommand
from apps.datajud_client.services import consultar_processo

class Command(BaseCommand):
    help = "Consulta um número CNJ em múltiplos tribunais DataJud"

    def add_arguments(self, parser):
        parser.add_argument("numero_processo", type=str, help="Número CNJ (formato completo)")

    def handle(self, *args, **options):
        numero = options["numero_processo"]
        resultados = consultar_processo(numero)

        if resultados:
            self.stdout.write(
                self.style.SUCCESS(f"\n🔍 {len(resultados)} processo(s) encontrado(s):\n")
            )
            for idx, proc in enumerate(resultados, start=1):
                self.stdout.write(self.style.NOTICE(f"--- Processo {idx} ---"))
                self.stdout.write(json.dumps(proc, indent=2, ensure_ascii=False))  # 🔍 mostra tudo formatado
                self.stdout.write("\n")
        else:
            self.stdout.write(self.style.WARNING("Nenhum processo encontrado."))
