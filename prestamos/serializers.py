from rest_framework import serializers
from .models import Prestamo

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'

#-----------------------------------------------------------------------------------------------

    def validate_solicitante(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'El solicitante es obligatorio...'
            )
        return value.strip()

#-----------------------------------------------------------------------------------------------
    # En un PATCH no llegan todos los campos, los que faltan se toman del préstamo actual

    def validate(self, data):
        equipo = data.get('equipo', getattr(self.instance, 'equipo', None))
        fecha_prestamo = data.get('fecha_prestamo', getattr(self.instance, 'fecha_prestamo', None))
        fecha_devolucion = data.get('fecha_devolucion', getattr(self.instance, 'fecha_devolucion', None))
        estado = data.get('estado', getattr(self.instance, 'estado', 'ACTIVO'))

        if fecha_prestamo and fecha_devolucion and fecha_devolucion < fecha_prestamo:
            raise serializers.ValidationError({
                'fecha_devolucion': 'La fecha de devolución no puede ser anterior a la fecha de préstamo...'
            })

        if estado == 'ACTIVO':
            if not equipo.activo or equipo.estado == 'MANTENIMIENTO':
                raise serializers.ValidationError({
                    'equipo': 'El equipo está inactivo o en mantenimiento, no puede tener un préstamo activo...'
                })

            prestamos_activos = Prestamo.objects.filter(equipo=equipo, estado='ACTIVO')
            if self.instance:
                prestamos_activos = prestamos_activos.exclude(id=self.instance.id)

            if prestamos_activos.exists():
                raise serializers.ValidationError({
                    'equipo': 'Este equipo ya tiene un préstamo activo...'
                })

        return data

#-----------------------------------------------------------------------------------------------
