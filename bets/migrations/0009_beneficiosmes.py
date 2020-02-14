# Generated by Django 3.0.3 on 2020-02-11 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0008_auto_20200210_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficiosMes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('capital_inicial', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ganancias_brutas', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ganancias_netas', models.DecimalField(decimal_places=2, max_digits=15)),
                ('porcentaje_beneficio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('porcentaje_beneficio_frente_al_inicial', models.DecimalField(decimal_places=2, max_digits=15)),
                ('temporada', models.IntegerField(default=0)),
                ('mes', models.IntegerField(default=0)),
            ],
        ),
    ]
