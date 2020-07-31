from rest_framework import viewsets
from rest_framework.response import Response

from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
