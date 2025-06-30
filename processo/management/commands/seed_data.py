from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

# IMPORTS de cada app específico
from processo.models import Processo
from movimentacao.models import Movimentacao
from parte.models import Parte
from tribunais.models import Tribunal

from faker import Faker
import random

fake = Faker("pt_BR")

User = get_user_model()


def gerar_numero_processo():
    nnnnnnn = str(random.randint(1000000, 9999999))
    dd = str(random.randint(10, 99))
    aaaa = str(random.randint(2000, timezone.now().year))
    j = str(random.randint(1, 9))
    tr = str(random.randint(10, 99))
    oooo = str(random.randint(1000, 9999))
    return f"{nnnnnnn}-{dd}.{aaaa}.{j}.{tr}.{oooo}"


class Command(BaseCommand):
    help = "Popula o banco de dados com dados de exemplo"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Iniciando..."))

        # Criar Tribunais
        tribunais = []
        for _ in range(5):
            tribunal = Tribunal.objects.create(
                sigla=fake.lexify(text="TR-??"),
                nome=f"Tribunal de Justiça {fake.state_abbr()}",
                estado=fake.state_abbr(),
                api_endpoint=fake.url(),
                api_tipo=random.choice(["REST", "SOAP"]),
            )
            tribunais.append(tribunal)

        # Criar Usuários
        usuarios = []
        for i in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="123456"
            )
            usuarios.append(user)

        # Criar Processos
        processos = []
        for i in range(50):
            numero_processo = gerar_numero_processo()
            processo = Processo.objects.create(
                numero_processo=numero_processo,
                tribunal=random.choice(tribunais).nome,  # se for FK, mude para .tribunal
                classe_processual=fake.word(),
                assunto=fake.sentence(nb_words=3),
                data_distribuicao=fake.date_this_decade(),
                orgao_julgador=fake.company(),
                valor_causa=round(random.uniform(1000, 100000), 2),
                situacao_atual=random.choice([s[0] for s in Processo.SITUACAO_CHOICES]),
                ultima_atualizacao=timezone.now(),
                usuario=random.choice(usuarios),
            )
            processos.append(processo)

        # Criar Partes
        for processo in processos:
            qtd_partes = random.randint(1, 4)
            for _ in range(qtd_partes):
                Parte.objects.create(
                    processo=processo,
                    nome=fake.name(),
                    tipo_parte=random.choice([tp[0] for tp in Parte.TIPO_PARTE_CHOICES]),
                    documento=fake.cpf(),
                )

        # Criar Movimentações
        for processo in processos:
            qtd_mov = random.randint(2, 6)
            for _ in range(qtd_mov):
                Movimentacao.objects.create(
                    processo=processo,
                    data_movimentacao=fake.date_time_this_year(),
                    tipo_movimentacao=fake.word(),
                    descricao=fake.sentence(nb_words=10),
                    responsavel=fake.name(),
                )

        self.stdout.write(self.style.SUCCESS("Dados criados com sucesso."))
