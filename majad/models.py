from django.db import models


class Administrador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)

    departamento = models.IntegerField(null=False)

    class Meta:
        ordering = ('departamento', 'nombre', 'apellido')
