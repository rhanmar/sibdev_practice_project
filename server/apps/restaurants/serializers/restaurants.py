from rest_framework import serializers

from apps.restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'photo', 'opening_time', 'closing_time', 'address', 'point', 'owner', 'average_cost', 'dishes')
