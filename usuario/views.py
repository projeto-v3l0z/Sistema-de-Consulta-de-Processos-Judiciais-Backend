from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import PodeCadastrarProcessos, PodeVisualizarProcessos
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return super().get_permissions()
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  

#Para testes
class RotaProtegidaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            return Response({
                "mensagem": f"Olá {request.user.username}, você está autenticado com JWT!"
            })

#View que usei pra testar o rate limit e o cache
from django.views.decorators.cache import cache_page

@api_view(["GET"])
@cache_page(30)                      # 30 s de cache
@ratelimit(key="ip", rate="1/m", block=True)  
def hello_world(request):
    print(">>> executou a view (só aparece 1x a cada 30 s)")
    return Response({"message": "Olá, mundo!"})


# apenas testando as permissões
@api_view(['GET'])
@permission_classes([IsAuthenticated, PodeCadastrarProcessos])
def teste(request):
    if request.user.groups.filter(name='Operador').exists():
        return HttpResponse("Você tem permissão.")
    else:
        return HttpResponse("Você não tem permissão.")