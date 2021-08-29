import django_filters
from django.db.models import Count, QuerySet

from api.models import Menu


class MenuFilterSet(django_filters.FilterSet):

    dishes_count = django_filters.CharFilter(method='dishes_count_filter')

    class Meta:

        model = Menu
        fields = {
            'name': ['exact', 'icontains'],
            'added_date': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
            'modified_date': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
        }

    def dishes_count_filter(self, queryset, _, value) -> QuerySet:
        return queryset.annotate(dishes_count=Count('dishes')).filter(
            dishes_count=value
        )
