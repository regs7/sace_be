from rest_framework import serializers

from core.models import CentroEducativo, Municipio, Persona, Alumno


class CentroEducativoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroEducativo
        fields = ('id', 'codigo', 'nombre')


class MunicipioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('id', 'departamento_codigo', 'codigo', 'nombre')


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = (
            'id',
            'identidad',
            'nombre',
            'apellido',
            'direccion',
            'telefonos',
            'fecha_nacimiento'
        )


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        depth = 1
        fields = ('persona',)
