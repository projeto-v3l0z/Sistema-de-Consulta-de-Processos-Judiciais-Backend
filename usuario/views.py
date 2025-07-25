from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import PodeCadastrarProcessos, PodeVisualizarProcessos
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from core.ratelimit_preset import Generico 


from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return super().get_permissions()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })



#Para testes

class RotaProtegidaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            return Response({
                "mensagem": f"Olá {request.user.username}, você está autenticado com JWT!"
            })

#View que usei pra testar o rate limit e o cache
 # Importando o preset personalizado

@api_view(["GET"])
@cache_page(30) # 30 s de cache
@ratelimit(key="ip", rate=Generico, block=True)
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
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def login_page_view(request):
    return render(request, 'usuario/login.html')