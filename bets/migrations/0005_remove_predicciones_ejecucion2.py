# Generated by Django 3.1.dev20191121095405 on 2020-01-23 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0004_predicciones_ejecucion2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predicciones',
            name='ejecucion2',
        ),
    ]
