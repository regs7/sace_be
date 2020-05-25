from django.contrib.auth.models import User
from django.db import models


class Administrador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)

    departamento = models.IntegerField(null=False)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('departamento', 'nombre', 'apellido')

    @property
    def correo(self):
        return self.usuario.email


class Coordinador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)

    departamento = models.IntegerField(null=False)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('departamento', 'nombre', 'apellido')

    @property
    def correo(self):
        return self.usuario.email


class CentroReferencia(models.Model):
    sede = models.IntegerField(null=False)
    coordinador = models.ForeignKey('Coordinador', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=256)
    municipio = models.IntegerField(null=False)
    direccion = models.TextField()

    class Meta:
        ordering = ('nombre', 'municipio',)


class Clase(models.Model):
    codigo = models.CharField(max_length=16, unique=True, null=False)
    nombre = models.CharField(max_length=128, null=False)
    descripcion = models.TextField(default='')

    class Meta:
        ordering = ('codigo', 'nombre')


class MallaCurricular(models.Model):
    codigo = models.CharField(max_length=16, unique=True, null=False)
    nombre = models.CharField(max_length=128, null=False)

    clases = models.ManyToManyField(Clase)

    class Meta:
        ordering = ('codigo',)


class Grado(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    malla = models.ForeignKey(MallaCurricular, on_delete=models.PROTECT)

    class Meta:
        ordering = ('nombre',)
