from rest_framework import serializers

from api.models import Dish, Menu


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = Dish
        fields = (
            'pk',
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
        fields = ('pk', 'name', 'describe', 'created', 'modified', 'dishes')
        read_only_fields = ('modified', 'created')

    def __init__(self, *args, **kwargs) -> None:
        """Show dishes on detail menu view."""
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if (
            request
            and request.method == 'GET'
            and self.context['view'].action == 'retrieve'
        ):
            self.Meta.depth = 1
        else:
            self.Meta.depth = 0
