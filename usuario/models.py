from django.db import models

# Colocar essa classe dentro do modelo de usuário para que as permissões sejam criadas
class Meta:
    permissions = [
        ("pode_cadastrar_processo", "Pode cadastrar processo"), 
        ("pode_editar_processo", "Pode editar processo"),
        ("pode_excluir_processo", "Pode excluir processo"),
        ("pode_consultar_processo", "Pode consultar processo"),
    ]