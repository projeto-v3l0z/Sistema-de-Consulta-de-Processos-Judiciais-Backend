# tribunais/urls.py
from django.urls import path
from .views import TribunalListView, TribunalDetailView

urlpatterns = [
    path('tribunais/', TribunalListView.as_view(), name='tribunal-list'),
    path('tribunais/<uuid:id>/', TribunalDetailView.as_view(), name='tribunal-detail'),
]