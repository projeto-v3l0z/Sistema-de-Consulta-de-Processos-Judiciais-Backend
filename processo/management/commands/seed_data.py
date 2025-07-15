# processos/management/commands/seed_processos.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from faker import Faker
import random, datetime

from processo.models import Processo, SituacaoProcesso
faker = Faker("pt_BR")
Faker.seed(42)

# ────────────────────────────────────────────────────────────────
# Utilidades para gerar um número CNJ “crível”
# Ex.: 1234567-89.2024.8.26.0100 (TJ‑SP / Foro Central)
# ────────────────────────────────────────────────────────────────
def gerar_numero_cnj(ano=None, tribunal_cod="26", foro_cod="0100"):
    """Gera um número CNJ no formato NNNNNNN-DD.AAAA.8.TT.FFFF."""
    nnnnnnn = faker.random_int(1000000, 9999999)
    dd = faker.random_int(10, 99)               # dígitos verificadores fake
    ano = ano or faker.random_int(2018, timezone.now().year)
    return f"{nnnnnnn}-{dd}.{ano}.8.{tribunal_cod}.{foro_cod}"

# Alguns tribunais estaduais (TT) + códigos de foro (FFFF)
TRIBUNAIS = {
    "26": {  # TJ‑SP
        "nome": "TJSP",
        "foros": ["0100", "0638", "0000"]  # central, barra funda, genérico
    },
    "19": {  # TJ‑RJ
        "nome": "TJRJ",
        "foros": ["0001", "0002", "0003"]
    },
    "14": {  # TJ‑PA
        "nome": "TJPA",
        "foros": ["0301", "0501"]
    },
    "13": {  # TJ‑MG
        "nome": "TJMG",
        "foros": ["0001", "0080"]
    },
}

CLASSES = [
    "Procedimento Comum Cível",
    "Ação Penal",
    "Ação Trabalhista",
    "Execução Fiscal",
    "Mandado de Segurança",
]

ASSUNTOS = [
    "Direito do Consumidor",
    "Responsabilidade Civil",
    "Fundo de Garantia",
    "Revisão de Benefícios",
    "Fraude Bancária",
    "Danos Morais",
]

ORGAOS = [
    "1ª Vara Cível",
    "2ª Vara Criminal",
    "3ª Vara do Trabalho",
    "Vara de Execuções Fiscais",
    "Vara Única",
]

SITUACOES = [choice[0] for choice in SituacaoProcesso.choices]

# ────────────────────────────────────────────────────────────────
# Comando de seed
# ────────────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = "Popula a tabela Processo com dados realistas fictícios."

    def add_arguments(self, parser):
        parser.add_argument(
            "--qtd",
            type=int,
            default=10000,
            help="Quantidade de processos a gerar (padrão: 300).",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        qtd = opts["qtd"]
        criados = []
        for _ in range(qtd):
            # Tribunal e foro
            tt, info = random.choice(list(TRIBUNAIS.items()))
            foro = random.choice(info["foros"])

            # Datas coerentes
            data_dist = faker.date_between_dates(
                date_start=datetime.date(2018, 1, 1),
                date_end=timezone.now().date()
            )
            ultima_atual = faker.date_time_between_dates(
                datetime_start=datetime.datetime.combine(data_dist, datetime.time.min),
                datetime_end=timezone.now()
            )

            criados.append(
                Processo(
                    numero_processo=gerar_numero_cnj(data_dist.year, tt, foro),
                    tribunal=info["nome"],
                    classe_processual=random.choice(CLASSES),
                    assunto=random.choice(ASSUNTOS),
                    data_distribuicao=data_dist,
                    orgao_julgador=random.choice(ORGAOS),
                    valor_causa=round(random.uniform(1_000, 500_000), 2),
                    situacao_atual=random.choice(SITUACOES),
                    ultima_atualizacao=ultima_atual,
                    parte_nome=faker.name(),
                    parte_cpf=faker.cpf(),      # já vem formatado 000.000.000‑00
                )
            )

        Processo.objects.bulk_create(criados)
        self.stdout.write(
            self.style.SUCCESS(f"{len(criados)} processos fictícios inseridos com sucesso!")
        )
