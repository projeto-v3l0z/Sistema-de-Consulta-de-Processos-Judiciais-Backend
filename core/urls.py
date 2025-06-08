from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuario.urls')),  
    path('api/processos/', include('processo.urls')),
    path('api/tribunais/', include('tribunais.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
