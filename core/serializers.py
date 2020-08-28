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
            'nombre_completo',
            'direccion',
            'telefono',
            'fecha_nacimiento',
            'edad',
            'genero',
            'contacto'
        )
        read_only_fields = ['nombre_completo', 'edad']


class AlumnoSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Alumno
        fields = ('id', 'persona',)


class StudentTuitionSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    codigo = serializers.CharField()
    centro = serializers.CharField()
    curso = serializers.CharField()
    seccion = serializers.CharField()
    fecha = serializers.DateField()
