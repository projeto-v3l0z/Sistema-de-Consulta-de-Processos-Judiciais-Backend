from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  

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
