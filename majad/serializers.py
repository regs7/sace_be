from rest_framework import serializers

from core.models import Departamento
from majad.models import Administrador


class AdministradorSerializer(serializers.ModelSerializer):
    departamento_text = serializers.SerializerMethodField()

    class Meta:
        model = Administrador
        fields = ('nombre', 'apellido', 'departamento', 'departamento_text')
        read_only = ('departamento_text',)

    def get_departamento_text(self, obj):
        departamento = Departamento.objects.using('sace1').get(id=obj.departamento)
        return f'{departamento.codigo} - {departamento.nombre}'
