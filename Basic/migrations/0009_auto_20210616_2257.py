# Generated by Django 3.1.7 on 2021-06-17 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0008_auto_20210611_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataavm',
            name='api',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='bsw',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='corrienteVSD',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='gor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='pip',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='pruebaValida',
            field=models.CharField(choices=[('VALIDA', 'Valida'), ('PENDIE', 'Pendiente')], default='VALIDA', max_length=6),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='salinidad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='tasaAceite',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='tasaAgua',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='tasaGas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='tasaLiquido',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='tempCabeza',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='thp',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='velocidadBomba',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='dataavm',
            name='voltajeOutVSD',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
