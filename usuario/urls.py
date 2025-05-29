from django.urls import path
from .views import hello_world, RotaProtegidaView

urlpatterns = [
    path('hello/', hello_world),
    path('protegida/', RotaProtegidaView.as_view(), name='rota_protegida'),
    
]
