from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import serializers, status

from core.models import Departamento
from majad.models import Administrador, Coordinator


class AdministradorSerializer(serializers.ModelSerializer):
    departamento_text = serializers.SerializerMethodField()
    correo = serializers.CharField()

    class Meta:
        model = Administrador
        fields = ('id', 'nombre', 'apellido', 'departamento', 'departamento_text', 'correo')
        read_only = ('id',)

    def get_departamento_text(self, obj):
        departamento = Departamento.objects.using('sace1').get(id=obj.departamento)
        return f'{departamento.codigo} - {departamento.nombre}'

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


class CoordinatorSerializer(serializers.ModelSerializer):
    correo = serializers.CharField()

    class Meta:
        model = Coordinator
        fields = ('id', 'nombre', 'apellido', 'correo')
        read_only = ('id',)

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
            'departamento': request_user.administrador.departamento
        })
        obj = super(CoordinatorSerializer, self).create(validated_data)
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

        return super(CoordinatorSerializer, self).update(instance, validated_data)
