from django.db import models

class Beneficios(models.Model):
    dia = models.DateField()
    capital_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_brutas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_netas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio = models.DecimalField(max_digits = 15, decimal_places = 2) 
    def __unicode__(self):
        return self.dia

class Predicciones(models.Model):
    prediction = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    date = models.DateField()
    home_team = models.CharField(max_length = 50) 
    away_team = models.CharField(max_length = 50) 
    resultado = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    ejecucion = models.IntegerField(default = 0) 
    def __unicode__(self):
        return self.dia
