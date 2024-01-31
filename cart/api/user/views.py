from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.permissions import IsCustomer
from sales.models import Coupon
from sales.utils import coupon_utils
from sales.utils.process_order_utils import CouponNotFoundError
from . import serializers
from ...models import Wishlist, Cart


class UserWishlistAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Wishlist.objects.all()
    serializer_class = serializers.UserWishlistListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Wishlist.objects.filter(user=user).order_by('-created_at')
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserWishlistCreateSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super(UserWishlistAPI, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class UserCartAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Cart.objects.all()
    serializer_class = serializers.UserCartListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by('-created_at').select_related('product')
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCartCreateSerializer
        elif self.action == 'update':
            return serializers.UserCartUpdateSerializer
        return self.serializer_class

    @extend_schema(request=serializers.CartPriceCalculationSerializer)
    @action(detail=False, methods=['post'], url_path='calculate_price')
    def cart_price_calculation(self, request):
        user = self.request.user
        serializer = serializers.CartPriceCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coupon_code = serializer.validated_data.get('coupon_code', None)
        items = serializer.validated_data.get('items', [])
        subtotal = 0
        vat = 0
        discount = 0
        total = 0
        for item_data in items:
            cart_item_id = item_data.get('cart_item')
            quantity = item_data.get('quantity', 0)

            try:
                cart_item = Cart.objects.get(id=cart_item_id)
            except Cart.DoesNotExist:
                return Response({'detail': f'Cart item with ID {cart_item_id} not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            if cart_item.product_variant:
                subtotal += (cart_item.product.price + cart_item.product_variant.additional_price) * quantity
                vat += cart_item.product.get_vat_amount / 100 * (
                        cart_item.product.price + cart_item.product_variant.additional_price) * quantity
            else:
                subtotal += cart_item.product.price * quantity
                vat += cart_item.product.get_vat_amount / 100 * cart_item.product.price * quantity
        total = subtotal + vat
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                discount += coupon_utils.discount_after_coupon(subtotal, coupon, user)
            except Coupon.DoesNotExist:
                raise CouponNotFoundError('Coupon not found.')

        # Prepare the response data
        data = {
            'subtotal': subtotal,
            'vat': vat,
            'discount': discount,
            'total': total,
        }
        return Response(data, status=status.HTTP_200_OK)


    # @extend_schema(request=serializers.CartPriceCalculationSerializer)
    # @action(detail=False, methods=['post'], url_path='delete_cart')
    # def delete_cart(self, request):
    #     serializer = serializers.CartPriceCalculationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     cart_items_id = serializer.validated_data['cart_list']
    #     cart_items = Cart.objects.filter(id__in=cart_items_id)
    #
    #     if cart_items:
    #         for item in cart_items:
    #             Cart.objects.filter(id=item.id).delete()
    #         return Response({'detail': _('Cart items deleted successfully.')}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'detail': [_('Cart items does not exist')]}, status=status.HTTP_404_NOT_FOUND)
