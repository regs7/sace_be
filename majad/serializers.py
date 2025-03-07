from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import serializers, status

from core.models import Departamento, CentroEducativo, Municipio, Alumno
from majad.models import Administrador, Coordinador, CentroReferencia, Clase, MallaCurricular, Grado, Periodo, Matricula


class AdministradorSerializer(serializers.ModelSerializer):
    departamentos_text = serializers.SerializerMethodField()
    correo = serializers.CharField()

    class Meta:
        model = Administrador
        fields = ('id', 'nombre', 'apellido', 'departamentos', 'departamentos_text', 'correo')
        read_only = ('id',)

    def get_departamentos_text(self, obj):
        departamentos = Departamento.objects.using('sace1').filter(id__in=obj.departamentos)
        return [f'{departamento.codigo} - {departamento.nombre}' for departamento in departamentos]

    def create(self, validated_data):
        correo = validated_data.pop('correo')
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')

        try:
            group = Group.objects.get(name='majad_administrador')
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Rol administrador no encontrado", code=status.HTTP_501_NOT_IMPLEMENTED)

        try:
            usuario = User.objects.create(
                username=correo,
                email=correo,
                first_name=nombre,
                last_name=apellido,
                is_active=True
            )
        except ValidationError:
            raise serializers.ValidationError("Usuario con este correo ya existe", code=status.HTTP_406_NOT_ACCEPTABLE)

        usuario.groups.add(group)
        validated_data.update({
            'usuario': usuario
        })
        obj = super(AdministradorSerializer, self).create(validated_data)
        return obj

    def update(self, instance, validated_data):
        correo = validated_data.pop('correo')
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')

        usuario = instance.usuario
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.username = correo
        usuario.email = correo

        try:
            usuario.save()
        except IntegrityError:
            raise serializers.ValidationError("Usuario con este correo ya existe", code=status.HTTP_406_NOT_ACCEPTABLE)

        return super(AdministradorSerializer, self).update(instance, validated_data)


class CoordinadorSerializer(serializers.ModelSerializer):
    correo = serializers.CharField()
    centro_referencia_text = serializers.SerializerMethodField()

    class Meta:
        model = Coordinador
        fields = (
            'id',
            'nombre',
            'apellido',
            'correo',
            'centro_referencia',
            'centro_referencia_text'
        )
        read_only = ('id',)

    def get_centro_referencia_text(self, obj):
        return [cr.nombre for cr in obj.centro_referencia.all()]

    def create(self, validated_data):
        correo = validated_data.pop('correo')
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')
        centros_referencia = validated_data.get('centro_referencia')

        try:
            group = Group.objects.get(name='majad_coordinador')
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Rol coordinador no encontrado", code=status.HTTP_501_NOT_IMPLEMENTED)

        try:
            usuario = User.objects.create(
                username=correo,
                email=correo,
                first_name=nombre,
                last_name=apellido,
                is_active=True
            )
        except ValidationError:
            raise serializers.ValidationError("Usuario con este correo ya existe", code=status.HTTP_406_NOT_ACCEPTABLE)

        usuario.groups.add(group)

        validated_data.update({
            'usuario': usuario
        })

        obj = super(CoordinadorSerializer, self).create(validated_data)
        obj.centro_referencia.add(*centros_referencia)
        return obj

    def update(self, instance, validated_data):
        correo = validated_data.pop('correo')
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')
        centros_referencia = validated_data.get('centro_referencia')

        usuario = instance.usuario
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.username = correo
        usuario.email = correo

        try:
            usuario.save()
        except IntegrityError:
            raise serializers.ValidationError("Usuario con este correo ya existe", code=status.HTTP_406_NOT_ACCEPTABLE)

        instance.centro_referencia.clear()
        instance.centro_referencia.add(*centros_referencia)
        return super(CoordinadorSerializer, self).update(instance, validated_data)


class CentroReferenciaSerializer(serializers.ModelSerializer):
    municipio_text = serializers.SerializerMethodField()
    sede_text = serializers.SerializerMethodField()
    grados_text = serializers.SerializerMethodField()
    coordinador_name = serializers.SerializerMethodField()

    class Meta:
        model = CentroReferencia
        fields = (
            'id',
            'nombre',
            'sede',
            'sede_text',
            'municipio',
            'municipio_text',
            'direccion',
            'coordinador_name',
            'grados',
            'grados_text'
        )

    def get_municipio_text(self, obj):
        municipio = Municipio.objects.using('sace1').get(id=obj.municipio)
        return f'{municipio.codigo} - {municipio.nombre}'

    def get_sede_text(self, obj):
        sede = CentroEducativo.objects.using('sace1').get(id=obj.sede)
        return f'{sede.codigo} - {sede.nombre}'

    def get_coordinador_name(self, obj):
        coordinator_name = ','.join([f'{coordinador.nombre} {coordinador.apellido}' for coordinador in obj.coordinador_set.all()])
        return coordinator_name

    def get_grados_text(self, obj):
        return [grado.nombre for grado in obj.grados.all()]


class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = ('id', 'codigo', 'nombre', 'descripcion', 'horas')


class MallaCurricularSerializer(serializers.ModelSerializer):
    clases_text = serializers.SerializerMethodField()

    class Meta:
        model = MallaCurricular
        fields = ('id', 'codigo', 'nombre', 'clases', 'clases_text')

    def get_clases_text(self, obj):
        return [f'{clase.codigo} - {clase.nombre}' for clase in obj.clases.all()]


class GradoSerializer(serializers.ModelSerializer):
    malla_text = serializers.SerializerMethodField()

    class Meta:
        model = Grado
        fields = ('id', 'nombre', 'malla', 'malla_text')

    def get_malla_text(self, obj):
        malla = obj.malla
        return f'{malla.codigo} - {malla.nombre}'


class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = ('id', 'nombre', 'inicio', 'final',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False
            }
        }
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active'
        )

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        is_active = validated_data.get('is_active')

        if password:
            instance.set_password(password)

        instance.first_name = first_name
        instance.last_name = last_name
        instance.is_active = is_active

        instance.save()
        return instance


class MatriculaSerializer(serializers.ModelSerializer):
    alumno = serializers.SerializerMethodField()
    periodo_obj = serializers.SerializerMethodField()
    centro_referencia_obj = serializers.SerializerMethodField()
    grado_obj = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = (
            'id',
            'periodo',
            'periodo_obj',
            'centro_referencia',
            'centro_referencia_obj',
            'grado',
            'grado_obj',
            'alumno'
        )

    def get_alumno(self, obj):
        alumno = obj.alumno
        return {
            'id': alumno.id,
            'identidad': alumno.persona.identidad,
            'nombre': alumno.persona.nombre_completo,
            'edad': alumno.persona.edad
        }

    def get_periodo_obj(self, obj):
        return PeriodoSerializer(instance=obj.periodo).data

    def get_centro_referencia_obj(self, obj):
        return CentroReferenciaSerializer(instance=obj.centro_referencia).data

    def get_grado_obj(self, obj):
        return GradoSerializer(instance=obj.grado).data

    def create(self, validated_data):

        request = self.context.get("request")
        identidad = request.data.get("alumno")

        if identidad:
            try:
                alumno = Alumno.objects.get(persona__identidad=identidad)
                validated_data.update({
                    'alumno': alumno
                })
                return Matricula.objects.create(**validated_data)
            except Alumno.DoesNotExist:
                raise serializers.ValidationError(detail={'error': f'No se encontró alumno con identidad {identidad}'})
        raise serializers.ValidationError(detail={'error': 'Campo alumno requerido'})
