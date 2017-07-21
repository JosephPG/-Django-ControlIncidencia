from django.db import models
from django.utils import timezone

from usuario.models import Usuario, BackOffice, Asesor
from apps.cliente.models import Cliente


# Create your models here.


# Modelo Incidencia
class Incidencia(models.Model):
    def key_id():
        try:
            cod = int(Incidencia.objects.latest('id').id) + 1
            return cod
        except:
            return 100000000

    id = models.AutoField(primary_key=True, default=key_id)
    cod_asesor = models.ForeignKey(Asesor, null=False, blank=False,
                                   on_delete=models.CASCADE)
    cod_back = models.ForeignKey(BackOffice, null=True, blank=True,
                                 on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, null=False, blank=False)
    fecha_generada = models.DateTimeField(default=timezone.now, editable=False)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)


# Modelo Detalle de Incidencia
class DetalleIncidencia(models.Model):
    incidencia = models.ForeignKey(Incidencia, null=False, blank=False,
                                   on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=False, blank=False)
    detalle = models.TextField(blank=False, null=False)
    fecha_generada = models.DateTimeField(default=timezone.now)
