from django.db.models import Q, Value
from django.db.models.functions import Concat
from rest_framework import generics, viewsets

from core.models import CentroEducativo, Municipio, Alumno, Persona
from core.serializers import (
    CentroEducativoListSerializer,
    MunicipioListSerializer,
    PersonaSerializer, AlumnoSerializer
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
    serializer_class = AlumnoSerializer

    def perform_create(self, serializer):
        persona = PersonaSerializer(data=self.request.data)
        persona.is_valid(raise_exception=True)
        persona = persona.save()
        Alumno.objects.create(persona=persona)

    def perform_update(self, serializer):
        instance = self.get_object().persona
        persona = PersonaSerializer(instance, data=self.request.data)
        persona.is_valid(raise_exception=True)
        persona.save()

    def get_queryset(self):
        qs = super(AlumnoModelViewSet, self).get_queryset()
        query = self.request.query_params.get('query', '')
        if query:
            qs = qs.annotate(search_name=Concat('persona__nombre', Value(' '), 'persona__apellido'))
            qs = qs.filter(search_name__icontains=query)[:10]
        return qs
