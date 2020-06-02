# Generated by Django 3.0.5 on 2020-06-02 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('majad', '0013_centroreferencia_grados'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centroreferencia',
            name='coordinador',
        ),
        migrations.AddField(
            model_name='coordinador',
            name='centro_referencia',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='majad.CentroReferencia'),
        ),
    ]
