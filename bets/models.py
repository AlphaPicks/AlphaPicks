from django.db import models

# Create your models here.
class Beneficios(models.Model):
    dia = models.DateField()
    capital_inicial = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_brutas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    ganancias_netas = models.DecimalField(max_digits = 15, decimal_places = 2) 
    porcentaje_beneficio = models.DecimalField(max_digits = 15, decimal_places = 2) 
    def __unicode__(self):
        return self.dia

