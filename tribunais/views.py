<<<<<<< HEAD
#importações
from django.shortcuts import render
from rest_framework import generics
from .models import Tribunal
from .serializers import TribunalSerializer


#classes do tribunal

class TribunalListView(generics.ListAPIView):
    #view para lista os tribunais
    queryset = Tribunal.objects.all()
    serializer_class = TribunalSerializer

class TribunalDetailView(generics.RetrieveAPIView):
    #view para detalha o tribunal
    queryset = Tribunal.objects.all()
    serializer_class = TribunalSerializer
    lookup_field = 'id'
=======
#importações
from rest_framework import viewsets
from .models import Tribunal
from .serializers import TribunalSerializer


#classes do tribunal
class TribunalViewSet(viewsets.ModelViewSet):
    queryset = Tribunal.objects.all()
    serializer_class = TribunalSerializer
    lookup_field = 'id'
>>>>>>> 44615ad0c2942b9ced69d7a5bcc5db5abd1973e8
