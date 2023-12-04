from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _
from cart.models import Cart
from coreapp.models import Address
from delivery.models import OrderDelivery
from ..admin.serializers import AdminOrderItemSerializer
from ...models import Reason, Coupon, Order, OrderEvent


class UserCheckOutSerializer(serializers.Serializer):
    cart_items = serializers.ListField(allow_empty=False, allow_null=False)
    coupon_code = serializers.CharField(allow_null=True, required=False)
    address = serializers.IntegerField()
    payment_method = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context['request'].user
        address_id = attrs.get('address')

        try:
            cart_items = Cart.objects.filter(id__in=attrs.get('cart_items', []), user=user)
            if not cart_items or cart_items.count() != len(attrs.get('cart_items', [])):
                raise serializers.ValidationError({'cart_items': f"Some cart items not found."})

            for cart_item in cart_items:
                product = cart_item.product
                if not product.has_stock:
                    raise serializers.ValidationError({'cart_items': [f'{product.product_name} is out of stock.']})
            address = Address.objects.get(id=address_id, user=user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'detail': [_("Invalid address for the current user.")]})


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Address.objects.create(**validated_data, user=user)


class CustomerOrderListSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='get_item_count')
    tracking_number = serializers.CharField(source='invoice_no')

    class Meta:
        model = Order
        fields = ('id', 'tracking_number', 'item_count', 'created_at', 'total')


class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='get_item_count')
    tracking_number = serializers.CharField(source='invoice_no')
    customer_name = serializers.CharField(source='get_customer_name')
    customer_mobile = serializers.CharField(source='get_customer_mobile')
    customer_email = serializers.CharField(source='get_customer_email')
    order_items = AdminOrderItemSerializer(many=True, read_only=True, source='get_order_item')

    class Meta:
        model = Order
        fields = (
            "id", 'tracking_number', 'customer_name', 'customer_mobile', 'customer_email', 'item_count', 'order_items',
            'subtotal', 'vat', 'shipping_charge', 'customer_note', 'payment_method', 'discount', 'total',
            'shipping_address', 'created_at', 'coupon', 'customer'
        )


class CustomerOrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('cancel_reason', 'cancel_reason_note')


class CustomerOrderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEvent
        fields = '__all__'


class CustomerOrderTrackSerializer(serializers.ModelSerializer):
    events = CustomerOrderEventSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'invoice_no', 'estd_delivery_time', 'events', 'created_at')


class CustomerOrderLiveTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = ('order', 'estd_delivery_time', 'address', 'longitude', 'latitude')


class CustomerCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'coupon_title', 'coupon_code', 'discount_type', 'discount_amount', 'expire_date', 'is_active')


class CustomerReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('reason_type', 'reason_name')
