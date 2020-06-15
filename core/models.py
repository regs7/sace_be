from django.contrib.postgres.fields import ArrayField
from django.db import models


class CentroEducativo(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=14, null=False, unique=True)
    nombre = models.CharField(max_length=256, null=False)
    en_funcionamiento = models.IntegerField(null=False)

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
    identidad = models.CharField(max_length=32, unique=True, null=False)
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)
    fecha_nacimiento = models.DateField(null=False)
    direccion = models.TextField(default='')
    telefonos = ArrayField(models.CharField(max_length=16))

    class Meta:
        ordering = ('nombre', 'apellido',)


class Alumno(models.Model):
    persona = models.OneToOneField('core.Persona', on_delete=models.PROTECT)

    class Meta:
        ordering = ('persona',)
