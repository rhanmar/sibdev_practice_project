from django.db import models

from yandex_geocoder import Client

from django.contrib.auth.models import User


class Point(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # широта
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # долгота

    def __str__(self):
        return f"{str(self.latitude)}, {str(self.longitude)}"


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='uploads/', null=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    address = models.CharField(max_length=128, null=True)

    average_cost = models.FloatField(null=True)
    point = models.ForeignKey(Point, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.average_cost = 1001  # calc later
        if self.address:
            client = Client('eca8121e-a2ed-4826-9369-464e4ba79cab')
            longitude, latitude = client.coordinates(self.address)
            self.point = Point.objects.create(latitude=latitude, longitude=longitude)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
