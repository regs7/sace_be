# Generated by Django 3.0.5 on 2020-05-27 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('majad', '0008_auto_20200525_1917'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrador',
            options={'ordering': ('nombre', 'apellido')},
        ),
        migrations.RemoveField(
            model_name='administrador',
            name='departamento',
        ),
    ]
