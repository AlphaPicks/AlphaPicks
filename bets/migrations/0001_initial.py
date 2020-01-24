# Generated by Django 3.1.dev20191121095405 on 2020-01-22 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('capital_inicial', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ganancias_brutas', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ganancias_netas', models.DecimalField(decimal_places=2, max_digits=5)),
                ('porcentaje_beneficio', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]