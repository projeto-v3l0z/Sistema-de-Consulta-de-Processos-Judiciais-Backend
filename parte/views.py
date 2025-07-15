from rest_framework import generics
from .models import Parte
from .serializers import ParteSerializer

class ParteListCreateView(generics.ListCreateAPIView):
    queryset = Parte.objects.all()
    serializer_class = ParteSerializer

class ParteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parte.objects.all()
    serializer_class = ParteSerializer

class ParteListCreateView(generics.ListCreateAPIView):
    serializer_class = ParteSerializer
    def get_queryset(self):
        get_object_or_404(Processo, pk=self.kwargs['pk'])
        return Parte.objects.filter(processo_id=self.kwargs['pk'])
    def perform_create(self, serializer):
        processo = get_object_or_404(Processo, pk=self.kwargs['pk'])
        serializer.save(processo=processo)

class ParteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParteSerializer
    def get_queryset(self):
        return Parte.objects.filter(processo_id=self.kwargs['processo_pk'])