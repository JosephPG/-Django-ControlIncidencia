from django.db import models

# Create your models here.


# Modelo Tipo Servicio
class TipoServicio(models.Model):
    servicio = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.servicio)


# Modelo Cliente
class Cliente(models.Model):
    ruc = models.CharField(max_length=11, null=True, blank=True)
    dni = models.CharField(max_length=8, null=True, blank=True)
    nombre = models.CharField(max_length=80, null=True, blank=True)
    ape_pat = models.CharField(max_length=25, null=True, blank=True)
    ape_mat = models.CharField(max_length=25, null=True, blank=True)
    razon_social = models.CharField(max_length=30, null=True, blank=True)
    servicio = models.ManyToManyField(TipoServicio)

    def __str__(self):
        return '{} {}'.format(self.ruc, self.dni)
