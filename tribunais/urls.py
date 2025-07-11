<<<<<<< HEAD
from django.urls import path
from .views import TribunalListView, TribunalDetailView
=======
# tribunais/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TribunalViewSet


router = DefaultRouter()
router.register(r'tribunais', TribunalViewSet, basename='tribunal')
>>>>>>> 44615ad0c2942b9ced69d7a5bcc5db5abd1973e8

urlpatterns = [
    path('', TribunalListView.as_view(), name='tribunal-list'),
    path('<uuid:id>/', TribunalDetailView.as_view(), name='tribunal-detail'),
]