from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def initialize_permissions_and_groups(): # Função para inicializar permissões e grupos
    User = apps.get_model('usuario', 'User') # Importa o modelo User personalizado
    try:
        content_type = ContentType.objects.get(app_label='usuario', model='user') # Obtém o ContentType do modelo User
    except ContentType.DoesNotExist:
        print("ContentType para o modelo 'User' não existe. Certifique-se de que as migrações foram aplicadas.")
        return

    criar_permissões = [
        {'codename': 'cadastrar_processos', 'name': 'Pode cadastrar processos'},
        {'codename': 'editar_processos', 'name': 'Pode editar processos'},
        {'codename': 'visualizar_processos', 'name': 'Pode visualizar processos'},
        {'codename': 'excluir_processos', 'name': 'Pode excluir processos'},
    ]

    permissões_criadas = []
    for perm in criar_permissões: 
        permission, _ = Permission.objects.get_or_create(
            codename=perm['codename'],
            name=perm['name'],
            content_type=content_type
        )
        permissões_criadas.append(permission)

    operator_group, _ = Group.objects.get_or_create(name='Operador')
    for permission in permissões_criadas:
        operator_group.permissions.add(permission)

    user_group, _ = Group.objects.get_or_create(name='Usuário Comum')
    for permission in permissões_criadas:
        if permission.codename == 'visualizar_processos':
            user_group.permissions.add(permission)