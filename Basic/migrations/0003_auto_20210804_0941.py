# Generated by Django 3.1.7 on 2021-08-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0002_tasktracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktracker',
            name='type_error',
            field=models.TextField(blank=True, null=True),
        ),
    ]
