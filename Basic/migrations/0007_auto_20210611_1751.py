# Generated by Django 3.1.7 on 2021-06-11 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0006_auto_20210611_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataavm',
            name='pozo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sarta', to='Basic.pozo'),
        ),
    ]
