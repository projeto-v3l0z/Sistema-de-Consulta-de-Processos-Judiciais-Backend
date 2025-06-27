# tribunais/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TribunalViewSet


router = DefaultRouter()
router.register(r'tribunais', TribunalViewSet, basename='tribunal')

urlpatterns = [
    path('', TribunalListView.as_view(), name='tribunal-list'),
    path('<uuid:id>/', TribunalDetailView.as_view(), name='tribunal-detail'),
]