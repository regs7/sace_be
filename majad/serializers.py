from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import serializers, status

from core.models import Departamento, CentroEducativo, Municipio
from majad.models import Administrador, Coordinador, CentroReferencia, Clase, MallaCurricular, Grado, Periodo


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
                last_name=apellido
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
    centro_referencia_text = serializers.SerializerMethodField()
    correo = serializers.CharField()

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
        return obj.centro_referencia.nombre

    def create(self, validated_data):
        request_user = self.context.get('request').user

        correo = validated_data.pop('correo')
        nombre = validated_data.get('nombre')
        apellido = validated_data.get('apellido')

        try:
            group = Group.objects.get(name='majad_coordinador')
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Rol coordinador no encontrado", code=status.HTTP_501_NOT_IMPLEMENTED)

        try:
            usuario = User.objects.create(
                username=correo,
                email=correo,
                first_name=nombre,
                last_name=apellido
            )
        except ValidationError:
            raise serializers.ValidationError("Usuario con este correo ya existe", code=status.HTTP_406_NOT_ACCEPTABLE)

        usuario.groups.add(group)

        validated_data.update({
            'usuario': usuario,
            'departamentos': request_user.administrador.departamentos
        })
        obj = super(CoordinadorSerializer, self).create(validated_data)
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
        coordinator_name = '-'
        if getattr(obj, 'coordinador', False):
            coordinator_name = f'{obj.coordinador.nombre} {obj.coordinador.apellido}'
        return coordinator_name

    def get_grados_text(self, obj):
        return [grado.nombre for grado in obj.grados.all()]


class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = ('id', 'codigo', 'nombre', 'descripcion')


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
