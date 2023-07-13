from rest_framework import serializers

from user.serializers import UserFKSerializer
from vehicle.models import Vehicle


# Información del la entidad que se mostrara al llamarlo usando su relación con otra entidad.
class VehicleFKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'plates')


class VehiclesSerializers(serializers.ModelSerializer):
    users = UserFKSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'plates', 'brand', 'colour', 'model', 'serialNumber', 'users', 'alive']


# El detalle del objeto
class VehicleDetailSerializers(serializers.ModelSerializer):
    users = UserFKSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'
