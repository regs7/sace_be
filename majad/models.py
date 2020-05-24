from django.contrib.auth.models import User
from django.db import models


class Administrador(models.Model):
    nombre = models.CharField(max_length=256, null=False)
    apellido = models.CharField(max_length=256, null=False)

    departamento = models.IntegerField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('departamento', 'nombre', 'apellido')

    @property
    def correo(self):
        return self.usuario.email
