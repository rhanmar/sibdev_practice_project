from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    food_energy = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.food_energy}"
