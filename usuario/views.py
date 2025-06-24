from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import PodeCadastrarProcessos, PodeVisualizarProcessos
from django.http import HttpResponse
from rest_framework.views import APIView  
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer





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

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Olá, mundo!"})

# apenas testando as permissões
@api_view(['GET'])
@permission_classes([IsAuthenticated, PodeCadastrarProcessos])
def teste(request):
    if request.user.groups.filter(name='Operador').exists():
        return HttpResponse("Você tem permissão.")
    else:
        return HttpResponse("Você não tem permissão.")