from django_filters import rest_framework as dj_filters

from inventory.models import Category, Brand


class BrandFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Brand
        fields = ('name',)


class CategoryFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ('parent', 'name')
