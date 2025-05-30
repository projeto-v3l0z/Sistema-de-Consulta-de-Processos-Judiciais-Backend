from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# Modelo de usuário personalizado para fins de teste (substituir depois)
class User(AbstractUser):
    # . . .
    # Campos vão aqui
    # . . .
            
    def assign_default_groups_and_permissions(self):
        from django.contrib.auth.models import Group
        """
        Atribuindo grupos e permissões padrões ao usuário
        durante sua criação.
        """
        # Obtendo ou criando o grupo "Operador"
        operator_group, _ = Group.objects.get_or_create(name='Operador')
        # Obtendo ou criando o grupo "Usuário Comum"
        user_group, _ = Group.objects.get_or_create(name='Usuário Comum')

        # Adicionando o usuário ao grupo "Usuário Comum" por padrão
        if not self.groups.exists():  # Apenas adiciona se o usuário não tiver grupos
            user_group.user_set.add(self)

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
