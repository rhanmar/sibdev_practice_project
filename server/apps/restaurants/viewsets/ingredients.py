from rest_framework import viewsets
from rest_framework import mixins

from apps.restaurants.serializers import IngredientSerializer
from apps.restaurants.models import Ingredient

from url_filter.integrations.drf import DjangoFilterBackend


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = '__all__'
