from django.db import models

class Equipo(models.Model):
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('MANTENIMIENTO', 'Mantenimiento'),
    ]
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
