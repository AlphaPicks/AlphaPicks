# Generated by Django 3.1.dev20191121095405 on 2020-01-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0005_remove_predicciones_ejecucion2'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficios',
            name='porcentaje_beneficio_frente_al_inicial',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
    ]