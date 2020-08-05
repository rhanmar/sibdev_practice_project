from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apps.restaurants.models import Dish


@receiver(m2m_changed, sender=Dish.ingredients.through)
def calc_dish_calories(sender, **kwargs):
    ingredients = kwargs['instance'].ingredients.all()
    calories = [ingredient.food_energy for ingredient in ingredients]
    calories = sum(calories)
    kwargs['instance'].dish_calories = calories
    kwargs['instance'].save()
