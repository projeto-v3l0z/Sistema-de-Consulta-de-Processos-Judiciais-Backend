from django.urls import path
from .views import hello_world, teste

urlpatterns = [
    path('hello/', hello_world),
    path('teste/', teste), # apenas teste de permissão
]
