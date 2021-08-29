from rest_framework import serializers

from api.models import Dish, Menu


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Dish
        fields = '__all__'
        read_only_fields = ('modified_date', 'added_date')
        extra_kwargs = {'menu': {'required': False}}


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Menu
        fields = '__all__'
        read_only_fields = ('modified_date', 'added_date')
        depth = 1
