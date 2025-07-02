from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, hello_world, RotaProtegidaView, teste, MyTokenObtainPairView, login_page_view


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('hello/', hello_world),
    path('protegida/', RotaProtegidaView.as_view(), name='rota_protegida'),
    
    path('login/', login_page_view, name='login_page'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('teste/', teste),  # apenas teste de permissão
]