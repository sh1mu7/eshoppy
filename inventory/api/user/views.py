from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as dj_filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from coreapp.permissions import IsCustomer
from sales.models import OrderItem
from . import serializers
from .. import filters
from ... import constants
from ...models import Brand, Category, Product, ProductReview, ProductVariant


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

    @action(detail=False, methods=['get'], url_path='new_arrival')
    def get_new_arrival(self, request):
        try:
            related_products = Product.objects.filter(is_active=True,
                                                      stock_status=constants.StockStatusChoices.IN_STOCK).order_by(
                '-created_at')[:14]
            serializer = serializers.NewArrivalProductSerializer(related_products, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': _("Invalid product selection")}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=None)
    @action(detail=True, methods=['get'], url_path='related_product')
    def get_related_product(self, request, pk=None):
        try:
            product = self.get_object()
            related_products = Product.objects.filter(
                Q(category=product.category) | Q(name__icontains=product.name) &
                Q(is_active=True, stock_status=constants.StockStatusChoices.IN_STOCK)
            ).exclude(id=product.id)
            serializer = serializers.CustomerProductListSerializer(related_products, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'detail': _("Invalid product selection")}, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(request=None)
    @action(detail=True, methods=['get'], url_path='calculate_price/(?P<variant_id>[^/.]+)')
    def calculate_price(self, request, pk=None, variant_id=None):
        try:
            product = self.get_object()
        except ObjectDoesNotExist:
            return Response({'detail': _("Invalid product selection")}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product_variant = ProductVariant.objects.get(id=variant_id, product=product)
            calculated_price = product.price + product_variant.additional_price
            data = {
                'calculated_price': calculated_price,
                'variant_id': product_variant.id,
                'vat_amount': product.vat,
                'reward_amount': product.reward_points
            }
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': _("Invalid product variant selection")}, status=status.HTTP_400_BAD_REQUEST)


class CustomerProductReviewAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = ProductReview.objects.all()
    serializer_class = serializers.CustomerProductReviewSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.ProductReviewFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CustomerProductReviewSerializer
        elif self.action == 'retrieve':
            return serializers.CustomerProductReviewDetailSerializer
        return self.serializer_class

    @extend_schema(request=None)
    @action(detail=False, methods=['get'], url_path='rating_counter/(?P<product_id>\d+)', permission_classes=[AllowAny])
    def get_rating_counter(self, request, product_id):
        try:
            queryset = ProductReview.objects.filter(product_id=product_id)
            rating_counts = queryset.values('rating').annotate(count=Count('rating'))
            data = {
                f'rating_{rating["rating"]}': rating['count']
                for rating in rating_counts
            }
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TopSellingProduct(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    queryset = OrderItem.objects.all()
    serializer_class = serializers.TopSellingSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.TopSelling
