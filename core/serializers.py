from rest_framework import serializers

from core.models import CentroEducativo


class CentroEducativoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroEducativo
        fields = ('id', 'codigo', 'nombre')
