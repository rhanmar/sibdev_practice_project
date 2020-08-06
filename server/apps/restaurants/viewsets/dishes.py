from rest_framework import viewsets

from apps.restaurants.serializers import DishSerializer
from apps.restaurants.models import Dish

from url_filter.integrations.drf import DjangoFilterBackend


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', 'photo', 'price', 'dish_calories', 'ingredients')
