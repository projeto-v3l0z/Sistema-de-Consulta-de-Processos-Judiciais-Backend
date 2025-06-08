from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, hello_world, teste

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('router/', include(router.urls)),
    path('hello/', hello_world),
    path('teste/', teste),  # apenas teste de permissão
]