# Generated by Django 3.1.7 on 2021-09-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic', '0003_auto_20210804_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='datastork',
            name='fluidoTotal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True),
        ),
    ]
