from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters

from coreapp.permissions import IsCustomer
from . import serializers
from .. import filters
from ... import constants
from ...models import Brand, Category, Product, ProductReview


class CustomerBrandAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = serializers.CustomerBrandSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.BrandFilter


class CustomerCategoryAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CustomerCategorySerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CategoryFilter


class CustomerProductAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Product.objects.filter(is_active=True, stock_status=constants.StockStatusChoices.IN_STOCK)
    serializer_class = serializers.CustomerProductListSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CustomerProductFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CustomerProductDetailSerializer
        return self.serializer_class

    @extend_schema(request=None)
    @action(detail=True, methods=['get'], url_path='related_product')
    def get_related_product(self, request, pk=None):
        try:
            product = self.get_object()
            related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
            serializer = serializers.CustomerProductListSerializer(related_products, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': _("Invalid login credentials")}, status=status.HTTP_400_BAD_REQUEST)

    #TODO: One extra action needed for calculating the price on varaint selection



class CustomerProductReviewAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = ProductReview.objects.all()
    serializer_class = serializers.CustomerProductReviewSerializer
