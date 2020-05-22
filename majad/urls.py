from django.urls import path

from majad.views import AdministradorListCreateView

app_name = 'majad'

urlpatterns = [
    path('administrator/', AdministradorListCreateView.as_view()),
]
