import time

from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status

from core.models import Departamento
from majad.models import Administrador


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

        obj = super(AdministradorSerializer, self).create(validated_data)
        obj.usuario = usuario
        obj.save()
        return obj
