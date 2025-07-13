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
