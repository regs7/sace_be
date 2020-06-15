# Generated by Django 3.0.5 on 2020-06-11 19:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_municipio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad', models.CharField(max_length=32, unique=True)),
                ('nombre', models.CharField(max_length=256)),
                ('apellido', models.CharField(max_length=256)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.TextField(default='')),
                ('telefonos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), size=None)),
            ],
            options={
                'ordering': ('nombre', 'apellido'),
            },
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Persona')),
            ],
            options={
                'ordering': ('persona',),
            },
        ),
    ]
