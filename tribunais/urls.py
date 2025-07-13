# tribunais/urls.py
from django.urls import path
from .views import TribunalListView, TribunalDetailView

urlpatterns = [
    path('', TribunalListView.as_view(), name='tribunal-list'),
    path('<uuid:id>/', TribunalDetailView.as_view(), name='tribunal-detail'),
]