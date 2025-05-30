# tribunais/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TribunalViewSet


router = DefaultRouter()
router.register(r'tribunais', TribunalViewSet, basename='tribunal')

urlpatterns = [
<<<<<<< HEAD
    path('', TribunalListView.as_view(), name='tribunal-list'),
    path('<uuid:id>/', TribunalDetailView.as_view(), name='tribunal-detail'),
=======
    path('', include(router.urls)),
>>>>>>> edcc590 (2 commit de tribunais com remoção de usuario e view7)
]