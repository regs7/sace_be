from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import Municipio


class Administrador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)
    departamentos = ArrayField(models.IntegerField(null=False))

    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('nombre', 'apellido')

    @property
    def correo(self):
        return self.usuario.email

    @property
    def municipios(self):
        municipios = Municipio.objects.using('sace1').filter(departamento_id__in=self.departamentos)
        return [municipio.id for municipio in municipios]


class Coordinador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)

    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    centro_referencia = models.ManyToManyField('majad.CentroReferencia')

    class Meta:
        ordering = ('nombre', 'apellido')

    @property
    def correo(self):
        return self.usuario.email


class CentroReferencia(models.Model):
    sede = models.IntegerField(null=False)
    nombre = models.CharField(max_length=256)
    municipio = models.IntegerField(null=False)
    direccion = models.TextField()

    grados = models.ManyToManyField('majad.Grado')

    class Meta:
        ordering = ('nombre', 'municipio',)


class Clase(models.Model):
    codigo = models.CharField(max_length=64, unique=True, null=False)
    nombre = models.CharField(max_length=128, null=False)
    descripcion = models.TextField(default='')
    horas = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('codigo', 'nombre')


class MallaCurricular(models.Model):
    codigo = models.CharField(max_length=64, unique=True, null=False)
    nombre = models.CharField(max_length=128, null=False)

    clases = models.ManyToManyField(Clase)

    class Meta:
        ordering = ('codigo',)


class Grado(models.Model):
    nombre = models.CharField(max_length=128, unique=True)
    malla = models.ForeignKey(MallaCurricular, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-id',)


class Periodo(models.Model):
    nombre = models.CharField(max_length=128, unique=True)
    inicio = models.DateField()
    final = models.DateField()

    class Meta:
        ordering = ('inicio',)


class Matricula(models.Model):
    alumno = models.ForeignKey('core.Alumno', on_delete=models.PROTECT)
    grado = models.ForeignKey('majad.Grado', on_delete=models.PROTECT)
    centro_referencia = models.ForeignKey('majad.CentroReferencia', on_delete=models.PROTECT)
    periodo = models.ForeignKey('majad.Periodo', on_delete=models.PROTECT)

    class Meta:
        ordering = ('-periodo', 'centro_referencia', 'grado')
