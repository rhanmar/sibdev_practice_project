from django.contrib import admin
from apps.restaurants.models import Restaurant, Dish, Ingredient


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'photo'
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'photo', 'price', 'dish_calories'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'food_energy'
    )
