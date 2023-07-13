from django.db import models
from user.models import User


class Vehicle(models.Model):
    plates = models.CharField(max_length=20, unique=True, null=False)
    brand = models.CharField(max_length=255, null=False)
    colour = models.CharField(max_length=50, null=False)
    model = models.CharField(max_length=255)
    serialNumber = models.CharField(max_length=100)
    alive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=254)
    createdDate = models.DateTimeField(auto_now_add=True)
    lastModifiedBy = models.CharField(max_length=254)
    lastModifiedDate = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(User, related_name='vehicles')

    def __str__(self):
        return self.plates