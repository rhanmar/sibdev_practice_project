from rest_framework import viewsets
from rest_framework import mixins

from apps.restaurants.serializers import IngredientSerializer
from apps.restaurants.models import Ingredient

from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
        Return the given ingredient.

    list:
        Return a list of all ingredients.
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'food_energy')
    permission_classes = (IsAuthenticatedOrReadOnly, )
