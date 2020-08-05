from django.db import models

from yandex_geocoder import Client

from django.contrib.auth.models import User
from .dishes import Dish
from config.settings.settings import YANDEX_GEOCODER_API_KEY


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

    average_cost = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    dishes = models.ManyToManyField(Dish)

    def save(self, *args, **kwargs):
        if self.address:
            client = Client(YANDEX_GEOCODER_API_KEY)
            longitude, latitude = client.coordinates(self.address)
            self.point, _ = Point.objects.get_or_create(latitude=latitude, longitude=longitude)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
