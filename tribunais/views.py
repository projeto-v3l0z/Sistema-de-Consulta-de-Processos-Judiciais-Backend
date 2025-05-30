#importações
from rest_framework import viewsets
from .models import Tribunal
from .serializers import TribunalSerializer


#classes do tribunal
class TribunalViewSet(viewsets.ModelViewSet):
    queryset = Tribunal.objects.all()
    serializer_class = TribunalSerializer
    lookup_field = 'id'
