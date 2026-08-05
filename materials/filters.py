from django_filters import rest_framework as filters

from materials.models import Ad


class AdFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', label='Поиск по названию')

    class Meta:
        model = Ad
        fields = ['title']
