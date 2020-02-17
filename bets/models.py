from django.db import models

class Beneficios(models.Model):
    dia = models.DateField()
    capital_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_brutas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_netas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio_frente_al_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    temporada = models.IntegerField(default = 0)
    objects = models.Manager()
    def __unicode__(self):
        return self.dia

class BeneficiosMes(models.Model):
    dia = models.DateField()
    capital_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_brutas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_netas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio_frente_al_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    temporada = models.IntegerField(default = 0)
    mes = models.IntegerField(default = 0)
    objects = models.Manager()
    def __unicode__(self):
        return self.dia

class Predicciones(models.Model):
    prediction = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    date = models.DateField()
    home_team = models.CharField(max_length = 50) 
    away_team = models.CharField(max_length = 50) 
    resultado = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    ejecucion = models.IntegerField(default = 0)
    temporada = models.IntegerField(default = 0)
    probabilidad = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    cuota = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    objects = models.Manager()
    def __unicode__(self):
        return self.prediction

class Historico(models.Model):
    prediction = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    date = models.DateField()
    home_team = models.CharField(max_length = 50) 
    away_team = models.CharField(max_length = 50) 
    resultado = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    cuotaEmpate = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0) 
    ejecucion = models.IntegerField(default = 0)
    temporada = models.IntegerField(default = 0)  
    objects = models.Manager()
    def __unicode__(self):
        return self.prediction
