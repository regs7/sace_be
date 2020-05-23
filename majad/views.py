from rest_framework import generics

from majad.models import Administrador
from majad.serializers import AdministradorSerializer


class AdministradorListCreateView(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class AdministradorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
