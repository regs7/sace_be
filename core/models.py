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


class MatriculaV1(models.Model):
    fecha = models.DateField()
    alumno_id = models.IntegerField()
    seccion_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'alumnos_matricula'

    @classmethod
    def historico_matricula(cls, identidad_estudiante):
        historico_matricula = cls.objects.using("sace1").raw(
            f"""
                SELECT
                       alumnos_matricula.id,
                       cuentas_persona.primer_nombre,
                       cuentas_persona.primer_apellido,
                       secretaria_centroeducativo.codigo,
                       secretaria_centroeducativo.nombre as centro,
                       secretaria_curso.nombre as curso,
                       centroeducativo_seccion.descripcion as seccion,
                       alumnos_matricula.fecha
                FROM alumnos_matricula
                INNER JOIN alumnos_alumno ON alumnos_alumno.id = alumnos_matricula.alumno_id
                INNER JOIN cuentas_persona ON cuentas_persona.id = alumnos_alumno.persona_id
                INNER JOIN centroeducativo_seccion ON centroeducativo_seccion.id  = alumnos_matricula.seccion_id
                INNER JOIN centroeducativo_mallacurricular ON centroeducativo_mallacurricular.id = centroeducativo_seccion.malla_curricular_id
                INNER JOIN secretaria_mallacurricularoficial ON secretaria_mallacurricularoficial.id = centroeducativo_mallacurricular.malla_oficial_id
                INNER JOIN secretaria_curso ON secretaria_curso.id = secretaria_mallacurricularoficial.curso_id
                INNER JOIN secretaria_centroeducativo on secretaria_centroeducativo.id = centroeducativo_mallacurricular.centro_id
                WHERE cuentas_persona.identidad = '{identidad_estudiante}'
                ORDER BY alumnos_matricula.fecha DESC;
            """)

        return [{
            'nombre': matricula.primer_nombre,
            'apellido': matricula.primer_apellido,
            'codigo': matricula.codigo,
            'centro': matricula.centro,
            'curso': matricula.curso,
            'seccion': matricula.seccion,
            'fecha': matricula.fecha
        } for matricula in historico_matricula]


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
