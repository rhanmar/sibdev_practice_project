from rest_framework import viewsets

from apps.restaurants.serializers import DishSerializer
from apps.restaurants.models import Dish

from url_filter.integrations.drf import DjangoFilterBackend
from apps.main.permissions import DishPermission


class DishViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return the given dish.

    list:
        Return a list of all dishes.

    create:
        Create a new dish.

    destroy:
        Delete a dish.

    update:
        Update a dish.

    partial_update:
        Update a dish.
    """
    serializer_class = DishSerializer
    queryset = Dish.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'photo', 'price', 'dish_calories', 'ingredients')
    permission_classes = (DishPermission, )
