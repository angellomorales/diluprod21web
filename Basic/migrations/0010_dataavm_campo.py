# Generated by Django 3.1.7 on 2021-06-22 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0009_auto_20210616_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataavm',
            name='campo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Basic.campo'),
        ),
    ]
