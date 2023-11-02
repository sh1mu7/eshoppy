from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response

from . import serializers
from .. import filters
from ...models import Brand, Category, VariantOption, VariantGroup, Product, ProductVariant


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


class AdminProductAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Product.objects.all()
    serializer_class = serializers.AdminProductCreateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdminProductListSerializer
        if self.action == 'retrieve':
            return serializers.AdminProductDetailSerializer
        return self.serializer_class
