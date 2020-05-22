from django.db.models import Q
from rest_framework import generics

from core.models import CentroEducativo
from core.serializers import CentroEducativoListSerializer


class CentroEducativoListView(generics.ListAPIView):
    queryset = CentroEducativo.objects.using('sace1').all()
    serializer_class = CentroEducativoListSerializer

    def get_queryset(self):
        qs = super(CentroEducativoListView, self).get_queryset()
        query = self.request.query_params.get('query')
        qs = qs.filter(Q(codigo__icontains=query) | Q(nombre__icontains=query))[:10]
        return qs
