from django.db import models

from .ingredients import Ingredient


class Dish(models.Model):
    name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='uploads/dishes', null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient)
    dish_calories = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name}"
