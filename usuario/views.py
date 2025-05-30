from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import PodeCadastrarProcessos, PodeVisualizarProcessos
from django.http import HttpResponse

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Olá, mundo!"}) 

# apenas testando as permissões
@permission_classes([IsAuthenticated, PodeCadastrarProcessos])
def teste(request):
    if request.user.groups.filter(name='Operador').exists():
        return HttpResponse("Você tem permissão.")
    else:
        return HttpResponse("Você não tem permissão.")