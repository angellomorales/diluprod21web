# Generated by Django 3.1.7 on 2021-11-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0010_auto_20211109_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pozoinyector',
            name='proceso',
            field=models.CharField(choices=[('Inyección de agua', 'Inyección de agua'), ('Inyección de polímero', 'Inyección de polímero')], default='Inyección de agua', max_length=25),
        ),
    ]