from django.db import models

from .ingredients import Ingredient


class Dish(models.Model):
    name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='uploads/dishes', null=True)
    price = models.FloatField()
    ingredients = models.ManyToManyField(Ingredient)
    dish_calories = models.FloatField(null=True)

    def __str__(self):
        return f"{self.name}"
