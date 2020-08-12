from rest_framework import viewsets

from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer

from url_filter.integrations.drf import DjangoFilterBackend

from apps.main.permissions import RestaurantPermission

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return the given restaurant.

    list:
        Return a list of all restaurants.

    create:
        Create a new restaurant.

    destroy:
        Delete a restaurant.

    update:
        Update a restaurant.

    partial_update:
        Update a restaurant.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'photo', 'opening_time', 'closing_time', 'address', 'point', 'owner', 'average_cost', 'dishes')
    permission_classes = (RestaurantPermission, )

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
