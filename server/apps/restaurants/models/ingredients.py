from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    food_energy = models.FloatField()

    def __str__(self):
        return f"{self.name} {self.food_energy}"
