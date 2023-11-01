from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, mixins
from django_filters import rest_framework as dj_filters
from . import serializers
from .. import filters
from ...models import Brand, Category, VariantOption, VariantGroup, Product


class AdminBrandAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Brand.objects.all()
    serializer_class = serializers.AdminBrandSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.BrandFilter


class AdminCategoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Category.objects.all()
    serializer_class = serializers.AdminCategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CategoryFilter


class AdminVariantGroupAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = VariantGroup.objects.all()
    serializer_class = serializers.AdminVariantGroupSerializer


class AdminVariantOptionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = VariantOption.objects.all()
    serializer_class = serializers.AdminVariantOptionSerializer


class AdminProductListAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = Product.objects.all()
    serializer_class = serializers.AdminProductListSerializer
