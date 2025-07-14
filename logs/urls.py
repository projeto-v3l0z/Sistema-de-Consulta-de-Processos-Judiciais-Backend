# logs/urls.py
from rest_framework.routers import DefaultRouter
from .views import ConsultaLogViewSet

router = DefaultRouter()
router.register(r'', ConsultaLogViewSet, basename='logs')  # base path vazio → /api/logs/

urlpatterns = router.urls
