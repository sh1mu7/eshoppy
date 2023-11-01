from coreapp.permissions import IsCustomer
from rest_framework import viewsets, mixins
from django_filters import rest_framework as dj_filters
from . import serializers
from .. import filters
from ...models import Brand, Category


class CustomerBrandAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    # permission_classes = [IsCustomer, ]
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = serializers.CustomerBrandSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.BrandFilter


class CustomerCategoryAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    # permission_classes = [IsCustomer, ]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CustomerCategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CategoryFilter
