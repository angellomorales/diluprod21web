# Generated by Django 3.1.7 on 2021-06-23 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataavm',
            options={'ordering': ['fecha']},
        ),
    ]