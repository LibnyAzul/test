from django.db import models

from vehicle.models import Vehicle
#from user.models import User


class Tracking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False)

    # Habilitar si queremos saber qué usuario conduce el vehículo.
    #  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    latitude = models.DecimalField(max_digits=15, decimal_places=12, null=False)
    longitude = models.DecimalField(max_digits=15, decimal_places=12, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking - Vehicle: {self.vehicle}, Latitude: {self.latitude}, Longitude: {self.longitude}, Created Date: {self.createdDate}"
