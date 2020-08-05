from django.db.models.signals import m2m_changed

from apps.restaurants.models import Dish


def calc_dish_calories(sender, **kwargs):
    ingredients = kwargs['instance'].ingredients.all()
    calories = [ingredient.food_energy for ingredient in ingredients]
    calories = sum(calories)
    kwargs['instance'].dish_calories = calories
    kwargs['instance'].save()


m2m_changed.connect(calc_dish_calories, sender=Dish.ingredients.through)

