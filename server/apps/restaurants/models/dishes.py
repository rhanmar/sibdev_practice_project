from django.db import models

from .ingredients import Ingredient


class Dish(models.Model):
    name = models.CharField(max_length=128, help_text='Обязательное. Название блюда')
    photo = models.ImageField(upload_to='uploads/dishes', null=True, help_text='Фотография блюда')
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text='Обязательное. Цена блюда')
    ingredients = models.ManyToManyField(Ingredient, help_text='Обязательное. Список ингредиентов блюда')
    dish_calories = models.DecimalField(max_digits=7, decimal_places=2, null=True, help_text='Калорийность блюда')

    def __str__(self):
        return f"{self.name}"
