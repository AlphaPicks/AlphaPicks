# Generated by Django 3.1.dev20191121095405 on 2020-01-23 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0003_auto_20200122_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicciones',
            name='ejecucion2',
            field=models.IntegerField(default=0),
        ),
    ]
