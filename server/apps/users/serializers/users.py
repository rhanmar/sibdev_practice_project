from rest_framework import serializers

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        try:
            token = Token.objects.get(user_id=obj.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)
        return token.key

    class Meta:
        model = User
        fields = ('username', 'password', 'token',)
        extra_kwargs = {'username': {'write_only': True},
                        'password': {'write_only': True}}
