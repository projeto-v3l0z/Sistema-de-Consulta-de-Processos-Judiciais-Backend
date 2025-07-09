from rest_framework.permissions import BasePermission

# Permissões personalizadas

class PodeCadastrarProcessos(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('usuario.cadastrar_processos')

class PodeEditarProcessos(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('usuario.editar_processos')

class PodeVisualizarProcessos(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('usuario.visualizar_processos')

class PodeExcluirProcessos(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('usuario.excluir_processos')