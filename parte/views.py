from rest_framework import generics
from .models import Parte
from .serializers import ParteSerializer

class ParteListCreateView(generics.ListCreateAPIView):
    queryset = Parte.objects.all()
    serializer_class = ParteSerializer

class ParteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parte.objects.all()
    serializer_class = ParteSerializer

