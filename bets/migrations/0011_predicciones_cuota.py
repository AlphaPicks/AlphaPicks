# Generated by Django 3.0.3 on 2020-02-17 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0010_predicciones_probabilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicciones',
            name='cuota',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
