from django.urls import path

from majad.views import (
    AdministradorListCreateView,
    AdministradorDetailView,
    CoordinatorListCreateView,
    CoordinatorDetailView
)

app_name = 'majad'

urlpatterns = [
    path('administrator/', AdministradorListCreateView.as_view()),
    path('administrator/<int:pk>', AdministradorDetailView.as_view()),

    path('coordinator/', CoordinatorListCreateView.as_view()),
    path('coordinator/<int:pk>', CoordinatorDetailView.as_view()),
]
