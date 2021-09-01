from rest_framework import serializers

from api.models import Dish, Menu


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Dish
        fields = (
            'name',
            'describe',
            'created',
            'modified',
            'price',
            'preparation_time',
            'vegetarian',
            'image',
        )
        read_only_fields = ('modified', 'created')
        extra_kwargs = {'menu': {'required': False}}


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Menu
        fields = ('name', 'describe', 'created', 'modified', 'dishes')
        read_only_fields = ('modified', 'created')
        depth = 1
