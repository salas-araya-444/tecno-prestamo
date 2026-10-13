from django.db import models
from equipos.models import Equipo

class Prestamo(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
    ]
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name="prestamos"
    )
    solicitante = models.CharField(max_length=100)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')

    def __str__(self):
        return f'{self.equipo} - {self.solicitante}'
