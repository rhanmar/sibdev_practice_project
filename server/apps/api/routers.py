from django.urls import path
from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UserViewSet
from apps.restaurants.viewsets import RestaurantViewSet, DishViewSet, IngredientViewSet

from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UserViewSet, basename='users')
router.register('restaurants', RestaurantViewSet, basename='restaurants')
router.register('dishes', DishViewSet, basename='dishes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='auth/token')
]

urlpatterns += router.urls
