from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.template.defaultfilters import date as date_filter
from django.utils.timesince import timesince


class CentroEducativo(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=14, null=False, unique=True)
    nombre = models.CharField(max_length=256, null=False)
    en_funcionamiento = models.IntegerField(null=False)
    departamento_id = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'secretaria_centroeducativo'
        ordering = ('codigo', 'nombre',)


class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=2, null=False, unique=True)
    nombre = models.CharField(max_length=128, null=False)

    class Meta:
        managed = False
        ordering = ('codigo', 'nombre',)
        db_table = 'secretaria_departamento'


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=2, null=False, unique=True)
    nombre = models.CharField(max_length=128, null=False)

    departamento_id = models.IntegerField(null=False)

    class Meta:
        managed = False
        ordering = ('codigo', 'nombre',)
        db_table = 'secretaria_municipio'

    @property
    def departamento_codigo(self):
        return Departamento.objects.using('sace1').get(pk=self.departamento_id).codigo


class Persona(models.Model):
    MASCULINO = 1
    FEMENINO = 2

    GENERO = (
        ("M", MASCULINO),
        ("F", FEMENINO)
    )

    identidad = models.CharField(max_length=32, unique=True, null=False)
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)
    fecha_nacimiento = models.DateField(null=False)
    direccion = models.TextField(default='', null=True)
    telefono = models.CharField(max_length=16)
    genero = models.CharField(max_length=1, choices=GENERO, null=False)
    contacto = models.TextField(default='')

    class Meta:
        ordering = ('nombre', 'apellido',)

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def edad(self):
        return f'{date_filter(self.fecha_nacimiento, "N d, Y")} {timesince(self.fecha_nacimiento)}'


class Alumno(models.Model):
    persona = models.OneToOneField('core.Persona', on_delete=models.PROTECT)

    class Meta:
        ordering = ('persona',)
