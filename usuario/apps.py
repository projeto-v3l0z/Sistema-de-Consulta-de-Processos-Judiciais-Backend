from django.apps import AppConfig

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuario'

    def ready(self): # tem que comentar isso aqui pras migrações rodarem kkkk 
        from .initialization import initialize_permissions_and_groups
        initialize_permissions_and_groups()