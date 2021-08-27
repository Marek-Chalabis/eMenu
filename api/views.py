
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet

from api.models import Menu, Dish
from api.serializers import MenuSerializer, DishSerializer

# TODO use decorators to change mixins permissions


class DishModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class MenuModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin, # todo public filter by not empty
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin, # todo public empty list
    GenericViewSet,
):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
