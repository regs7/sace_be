# Generated by Django 3.0.5 on 2020-05-28 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majad', '0012_coordinador_departamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroreferencia',
            name='grados',
            field=models.ManyToManyField(to='majad.Grado'),
        ),
    ]
