from apps.test.models import Test
from apps.test.serializers import TestSerializer

from rest_framework import mixins
from rest_framework import viewsets


class TestViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    App for first tests
    """
    serializer_class = TestSerializer
    queryset = Test.objects.all()
