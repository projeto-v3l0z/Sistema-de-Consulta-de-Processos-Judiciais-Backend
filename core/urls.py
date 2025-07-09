from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

from rest_framework_simplejwt.views import(
    TokenRefreshView,
    )

schema_view = get_schema_view(
    openapi.Info(
        title="API de Processos Jurídicos",
        default_version='v1',
        description="Documentação da API de Processos Jurídicos",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuario.urls')),  
    path('api/processos/', include('processo.urls')),
    path('api/tribunais/', include('tribunais.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
