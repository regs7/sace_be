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
