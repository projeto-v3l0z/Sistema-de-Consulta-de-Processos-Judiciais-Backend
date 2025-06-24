from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, hello_world, RotaProtegidaView,RegisterView, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', hello_world),
    path('protegida/', RotaProtegidaView.as_view(), name='rota_protegida'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
   # path('teste/', teste),  # apenas teste de permissão
]