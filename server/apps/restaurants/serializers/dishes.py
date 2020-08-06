from rest_framework import serializers

from apps.restaurants.models import Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name', 'photo', 'price', 'ingredients', 'dish_calories')
