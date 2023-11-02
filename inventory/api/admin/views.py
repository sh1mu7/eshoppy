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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            if serializer.validated_data.get('has_variant', False):
                variant_data = []
                product_variants = serializer.validated_data.get('product_variants', [])
                for item in product_variants:
                    variant = ProductVariant(**dict(item), product=product)
                    variant_data.append(variant)
                ProductVariant.objects.bulk_create(variant_data)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdminProductListSerializer
        return self.serializer_class
