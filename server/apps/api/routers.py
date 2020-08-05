from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UserViewSet
from apps.restaurants.viewsets import RestaurantViewSet, DishViewSet, IngredientViewSet


router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UserViewSet, basename='users')
router.register('restaurants', RestaurantViewSet, basename='restaurants')
router.register('dishes', DishViewSet, basename='dishes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
