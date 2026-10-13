from rest_framework import serializers
from .models import Equipo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

#-----------------------------------------------------------------------------------------------

    def validate_codigo(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'El código es obligatorio...'
            )
        return value.strip()

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'El nombre es obligatorio...'
            )
        return value.strip()

    def validate_categoria(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                'La categoría es obligatoria...'
            )
        return value.strip()

#-----------------------------------------------------------------------------------------------
