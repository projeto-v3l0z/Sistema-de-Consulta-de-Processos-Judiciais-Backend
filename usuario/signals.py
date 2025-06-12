from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .initialization import initialize_permissions_and_groups

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    from django.apps import apps
    if apps.is_installed('usuario'):
        initialize_permissions_and_groups()