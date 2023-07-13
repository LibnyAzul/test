from rest_framework import serializers

from tracking.models import Tracking
from vehicle.models import Vehicle
from vehicle.serializers import VehicleFKSerializer


# from user.serializers import UserFKSerializer
# from user.models import User

class TrackingSerializer(serializers.ModelSerializer):
    vehicle_plates = serializers.CharField(write_only=True)

    # Habilitar si queremos saber qué usuario conduce el vehículo.
    #  user_name = serializers.CharField(write_only=True)

    class Meta:
        model = Tracking
        # Add user_name
        fields = ['id', 'latitude', 'longitude', 'createdDate', 'vehicle_plates']

    def validate_vehicle_plates(self, value):
        try:
            vehicle = Vehicle.objects.get(plates=value)
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle with plates does not exist")

    # Habilitar si queremos saber qué usuario conduce el vehículo.
    # def velidate_user_name(self, value):
    #     try:
    #         user = User.objects.get(plates=value)
    #         return user
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("User with name does not exist")

    def create(self, validated_data):
        vehicle = validated_data.pop('vehicle_plates')
        # user = validated_data.pop('user_name')
        # Add user=user
        tracking = Tracking.objects.create(vehicle=vehicle, **validated_data)
        return tracking


class TrackingDetailSerializers(serializers.ModelSerializer):
    vehicle = VehicleFKSerializer(read_only=True)

    # Habilitar si queremos saber qué usuario conduce el vehículo.
    #  user = UserFKSerializer(many=True, read_only=True)

    class Meta:
        model = Tracking
        fields = '__all__'
