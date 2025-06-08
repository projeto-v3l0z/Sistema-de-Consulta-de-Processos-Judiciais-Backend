from django.urls import path
from .views import ParteListCreateView, ParteRetrieveUpdateDestroyView

urlpatterns = [
    path('partes/', ParteListCreateView.as_view(), name='parte-list-create'),
    path('partes/<uuid:pk>/', ParteRetrieveUpdateDestroyView.as_view(), name='parte-detail'),
]