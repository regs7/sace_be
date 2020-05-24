from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from majad.models import Administrador, Coordinator
from majad.serializers import AdministradorSerializer, CoordinatorSerializer


class AdministradorListCreateView(generics.ListCreateAPIView):
    queryset = Administrador.objects.select_related('usuario').all()
    serializer_class = AdministradorSerializer


class AdministradorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class CoordinatorListCreateView(generics.ListCreateAPIView):
    queryset = Coordinator.objects.select_related('usuario').all()
    serializer_class = CoordinatorSerializer
    permission_classes = [IsAuthenticated]


class CoordinatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer
