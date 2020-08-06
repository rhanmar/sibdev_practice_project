from rest_framework import mixins
from rest_framework import viewsets

from apps.users.serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    create:
        Create a new user.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
