from rest_framework import serializers

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(required=False)

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token}

    class Meta:
        model = User
        fields = ('username', 'password', 'token',)
        extra_kwargs = {'username': {'write_only': True},
                        'password': {'write_only': True}}
