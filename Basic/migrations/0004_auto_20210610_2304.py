# Generated by Django 3.1.7 on 2021-06-11 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0003_auto_20210610_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozo',
            name='estado',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Inactivo', max_length=8),
        ),
    ]
