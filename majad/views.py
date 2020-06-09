from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from majad.models import Administrador, Coordinador, CentroReferencia, Clase, MallaCurricular, Grado, Periodo
from majad.serializers import (
    AdministradorSerializer,
    CoordinadorSerializer,
    CentroReferenciaSerializer,
    ClaseSerializer,
    MallaCurricularSerializer,
    GradoSerializer, PeriodoSerializer
)


class AdministradorListCreateView(generics.ListCreateAPIView):
    queryset = Administrador.objects.select_related('usuario').all()
    serializer_class = AdministradorSerializer

    def get_queryset(self):
        qs = super(AdministradorListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        return qs


class AdministradorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class CoordinadorListCreateView(generics.ListCreateAPIView):
    queryset = Coordinador.objects.select_related('usuario').all()
    serializer_class = CoordinadorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(CoordinadorListCreateView, self).get_queryset()
        qs = qs.filter(
            nombre__icontains=self.request.query_params.get('query', ''),
            departamentos__contains=self.request.user.administrador.departamentos
        )
        return qs


class CoordinadorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer
    permission_classes = [IsAuthenticated]


class CentroReferenciaListCreateView(generics.ListCreateAPIView):
    queryset = CentroReferencia.objects.select_related('coordinador').all()
    serializer_class = CentroReferenciaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(CentroReferenciaListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        municipios = self.request.query_params.get('municipios', [])
        if municipios:
            qs = qs.filter(municipio__in=municipios.split(','))
        return qs


class CentroReferenciaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CentroReferencia.objects.all()
    serializer_class = CentroReferenciaSerializer
    permission_classes = [IsAuthenticated]


class ClaseListCreateView(generics.ListCreateAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(ClaseListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        return qs


class ClaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
    permission_classes = [IsAuthenticated]


class MallaCurricularListCreateView(generics.ListCreateAPIView):
    queryset = MallaCurricular.objects.all()
    serializer_class = MallaCurricularSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(MallaCurricularListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        return qs


class MallaCurricularDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MallaCurricular.objects.all()
    serializer_class = MallaCurricularSerializer
    permission_classes = [IsAuthenticated]


class GradoListCreateView(generics.ListCreateAPIView):
    queryset = Grado.objects.select_related('malla').all()
    serializer_class = GradoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(GradoListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        return qs


class GradoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grado.objects.select_related('malla').all()
    serializer_class = GradoSerializer
    permission_classes = [IsAuthenticated]


class PeriodoListCreateView(generics.ListCreateAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(PeriodoListCreateView, self).get_queryset()
        qs = qs.filter(nombre__icontains=self.request.query_params.get('query', ''))
        return qs


class PeriodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAuthenticated]
