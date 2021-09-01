from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import MenuFilterSet
from api.models import Dish, Menu
from api.permisions import MenuPermission
from api.serializers import DishSerializer, MenuSerializer


class DishModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class MenuModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Menu.objects.all().prefetch_related('dishes')  #
    serializer_class = MenuSerializer
    permission_classes = [MenuPermission]
    ordering_fields = ['name']
    filterset_class = MenuFilterSet

    def retrieve(self, request, *args, **kwargs) -> Response:
        """Not authorized users cannot see empty menus"""
        instance = self.get_object()
        if not instance.have_dishes and not request.user.is_authenticated:
            return Response(
                data={'detail': 'We are still working on this menu :)'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False, url_path='menus_with_dishes', url_name='menus_with_dishes'
    )
    def menus_with_dishes(self, request: Request) -> Response:
        queryset = self.filter_queryset(
            self.get_queryset().exclude(dishes__isnull=True)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)
