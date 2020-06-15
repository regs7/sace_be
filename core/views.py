from django.db.models import Q
from rest_framework import generics, viewsets

from core.models import CentroEducativo, Municipio, Alumno
from core.serializers import (
    CentroEducativoListSerializer,
    MunicipioListSerializer,
    PersonaSerializer
)


class CentroEducativoListView(generics.ListAPIView):
    queryset = CentroEducativo.objects.using('sace1').all()
    serializer_class = CentroEducativoListSerializer

    def get_queryset(self):
        qs = super(CentroEducativoListView, self).get_queryset()
        query = self.request.query_params.get('query')
        qs = qs.filter(Q(codigo__icontains=query) | Q(nombre__icontains=query))[:10]
        return qs


class MunicipioListView(generics.ListAPIView):
    queryset = Municipio.objects.using('sace1').all()
    serializer_class = MunicipioListSerializer

    def get_queryset(self):
        qs = super(MunicipioListView, self).get_queryset()
        query = self.request.query_params.get('query')
        qs = qs.filter(Q(codigo__icontains=query) | Q(nombre__icontains=query))[:10]
        return qs


class AlumnoModelViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.select_related('persona').all()
    serializer_class = PersonaSerializer

    def perform_create(self, serializer):
        persona = serializer.save()
        Alumno.objects.create(persona=persona)
