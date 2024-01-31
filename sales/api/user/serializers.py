from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from cart.models import Cart
from coreapp.models import Address
from delivery.models import OrderDelivery
from ..admin.serializers import AdminOrderItemSerializer
from ...models import Reason, Coupon, Order, OrderEvent, OrderReturn


class CartItemSerializer(serializers.Serializer):
    cart_item = serializers.IntegerField()
    quantity = serializers.IntegerField()


class UserCheckOutSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(allow_null=True, required=False)
    address = serializers.IntegerField()
    payment_method = serializers.IntegerField()
    items = serializers.ListField(
        child=CartItemSerializer()
    )
    customer_note = serializers.CharField(allow_null=True, required=False)

    def validate(self, attrs):
        user = self.context['request'].user
        address_id = attrs.get('address')
        try:
            cart_items = []
            for item in attrs.get('items', []):
                cart_item = item.get('cart_item')
                quantity = item.get('quantity')
                try:
                    cart_item = Cart.objects.get(id=cart_item, user=user)
                    product = cart_item.product
                    cart_item.quantity = quantity
                    if not product.has_stock:
                        raise serializers.ValidationError({'items': [f'{product} is out of stock.']})
                    if quantity > cart_item.quantity:
                        raise serializers.ValidationError(
                            {'items': [f'Insufficient stock for {product}.']})
                    cart_items.append(cart_item)
                except Cart.DoesNotExist:
                    raise serializers.ValidationError({'items': [f'Cart item with ID {cart_item} not found.']})
            address = Address.objects.get(id=address_id, user=user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'detail': [_("Invalid address for the current user.")]})


class CustomerAddressSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

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
        fields = (
            'id', 'tracking_number', 'item_count', 'order_status', 'order_stage', 'payment_status', 'created_at',
            'total'
        )


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
            'shipping_address', 'created_at', 'coupon', 'customer', 'order_status', 'order_stage', 'payment_status'
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


class CustomerReasonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'


class CustomerReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('reason_type', 'reason_name')


class CustomerOrderReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReturn
        fields = ('order', 'reason', 'image', 'refund_method', 'reason_detail')

    def validate(self, attrs):
        current_time = timezone.now()
        order_created_at = attrs['order'].created_at
        time_difference = current_time - order_created_at
        if time_difference.days > 7:
            raise serializers.ValidationError("Order must be created within the last 7 days to initiate a return.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        customer_mobile = user.mobile
        image = validated_data.pop('image')
        order_return = OrderReturn.objects.create(**validated_data, customer_mobile=customer_mobile, customer=user)
        order_return.image.set(image)
        return order_return
