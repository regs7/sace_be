from django.urls import path

from majad.views import (
    AdministradorListCreateView,
    AdministradorDetailView
)

app_name = 'majad'

urlpatterns = [
    path('administrator/', AdministradorListCreateView.as_view()),
    path('administrator/<int:pk>', AdministradorDetailView.as_view()),
]
