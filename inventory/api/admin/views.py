from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response

from . import serializers
from .. import filters
from ...models import Brand, Category, VariantOption, VariantGroup, Product, ProductVariant, ProductReview


class AdminBrandAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Brand.objects.all()
    serializer_class = serializers.AdminBrandSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.AdminBrandFilter


class AdminCategoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Category.objects.all()
    serializer_class = serializers.AdminCategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.AdminCategoryFilter


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
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.ProductFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdminProductListSerializer
        elif self.action == 'retrieve':
            return serializers.AdminProductDetailSerializer
        elif self.action == 'update':
            return serializers.AdminProductUpdateSerializer
        elif self.action == 'partial_update':
            return serializers.AdminProductUpdateSerializer
        return self.serializer_class


class AdminPromotionProductAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = Product.objects.all()
    serializer_class = serializers.AdminPromotionProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(has_promotion=True).order_by('id')
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AdminPromotionProductSerializer
        elif self.action == 'retrieve':
            return serializers.AdminPromotionProductDetailSerializer
        return self.serializer_class


class AdminProductReviewAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = ProductReview.objects.all()
    serializer_class = serializers.AdminProductReviewSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.ProductReviewFilter
