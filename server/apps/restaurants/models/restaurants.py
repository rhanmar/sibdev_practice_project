from django.db import models

from yandex_geocoder import Client

from django.contrib.auth.models import User
from .dishes import Dish

from config.settings.secret import yandex_geocoder_api


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

    point = models.ForeignKey(Point, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    average_cost = models.FloatField(null=True)
    dishes = models.ManyToManyField(Dish)

    def save(self, *args, **kwargs):
        print('!!!')
        if self.address:
            client = Client(yandex_geocoder_api)
            longitude, latitude = client.coordinates(self.address)
            self.point, created = Point.objects.get_or_create(latitude=latitude, longitude=longitude)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
