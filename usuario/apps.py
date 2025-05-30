from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuario'

    def ready(self):
        # Obter ContentType para o modelo associado às permissões
        content_type = ContentType.objects.get(app_label='usuario', model='User')

        # Criar permissões
        criar_permissões = [
            {'codename': 'cadastrar_processos', 'name': 'Pode cadastrar processos'},
            {'codename': 'editar_processos', 'name': 'Pode editar processos'},
            {'codename': 'visualizar_processos', 'name': 'Pode visualizar processos'},
            {'codename': 'excluir_processos', 'name': 'Pode excluir processos'},
        ]
        # Criando as permissões se não existirem
        permissões_criadas = []
        for perm in criar_permissões:
            permission, _ = Permission.objects.get_or_create(
                codename=perm['codename'],
                name=perm['name'],
                content_type=content_type
            )
            permissões_criadas.append(permission)

        # Criando o grupo Operador e adicionando todas as permissões
        operator_group, _ = Group.objects.get_or_create(name='Operador')
        for permission in permissões_criadas:
            operator_group.permissions.add(permission)
        
        # Criando o grupo Usuário Comum e adicionando apenas a permissão de visualizar processos
        user_group, _ = Group.objects.get_or_create(name='Usuário Comum')
        for permission in permissões_criadas:
            if permission.codename == 'visualizar_processos':
                user_group.permissions.add(permission)

    