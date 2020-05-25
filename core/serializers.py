from rest_framework import serializers

from core.models import CentroEducativo, Municipio


class CentroEducativoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroEducativo
        fields = ('id', 'codigo', 'nombre')


class MunicipioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id', 'codigo', 'nombre')
