from django.urls import path

from majad.views import (
    AdministradorListCreateView,
    AdministradorDetailView,
    CoordinadorListCreateView,
    CoordinadorDetailView,
    CentroReferenciaListCreateView,
    CentroReferenciaDetailView,
    ClaseListCreateView,
    ClaseDetailView
)

app_name = 'majad'

urlpatterns = [
    path('administrator/', AdministradorListCreateView.as_view()),
    path('administrator/<int:pk>', AdministradorDetailView.as_view()),

    path('coordinator/', CoordinadorListCreateView.as_view()),
    path('coordinator/<int:pk>', CoordinadorDetailView.as_view()),

    path('reference/school/', CentroReferenciaListCreateView.as_view()),
    path('reference/school/<int:pk>', CentroReferenciaDetailView.as_view()),

    path('clase/', ClaseListCreateView.as_view()),
    path('clase/<int:pk>', ClaseDetailView.as_view()),
]
