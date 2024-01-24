from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from coreapp import roles
from coreapp.models import User
from ...models import Reason, Coupon, OrderItem, Order, OrderEvent


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='get_product_name')
    image_url = serializers.CharField(source='get_product_image_url')

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'image_url', 'product_name', 'quantity', 'price', 'subtotal')


class AdminOrderListSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='get_item_count', read_only=True)
    customer_name = serializers.CharField(source='get_customer_name')
    customer_mobile = serializers.CharField(source='get_customer_mobile')

    class Meta:
        model = Order
        fields = (
            'created_at', 'id', 'invoice_no', 'customer_name', 'customer_mobile', 'item_count', 'order_status', 'total'
        )


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_customer_name')
    customer_mobile = serializers.CharField(source='get_customer_mobile')
    customer_email = serializers.CharField(source='get_customer_email')
    order_items = AdminOrderItemSerializer(many=True, read_only=True, source='get_order_item')
    order_event_status = serializers.CharField(source='get_order_event_status', read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", 'invoice_no', 'customer_name', 'customer_mobile', 'customer_email', 'order_items',
            'order_event_status', 'subtotal', 'vat', 'shipping_charge', 'customer_note', 'payment_method', 'discount',
            'total', 'shipping_address', 'created_at', 'coupon', 'customer'
        )


# class AdminOrderUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ('id', 'order_status', 'order_stage', 'cancel_reason', 'cancel_reason_note')
#

class AdminOrderCancel(serializers.Serializer):
    class Meta:
        model = Order
        fields = ('id', 'order_status', 'order_stage', 'cancel_reason', 'cancel_reason_note')


class AdminOrderAssignRider(serializers.Serializer):
    rider_id = serializers.IntegerField(allow_null=False, required=True)

    def validate(self, attrs):
        rider_id = attrs.get('rider_id')
        if rider_id and not User.objects.filter(id=rider_id, role=roles.UserRoles.DELIVERY_STAFF).exists():
            raise serializers.ValidationError({'user_id': [_('Invalid user id')]})
        return attrs


class AdminOrderChangePaymentStatus(serializers.Serializer):
    payment_status = serializers.IntegerField(allow_null=False, required=True)


class AdminOrderStatusChangeSerializer(serializers.Serializer):
    order = serializers.IntegerField(allow_null=False, required=True)
    note = serializers.IntegerField(allow_null=False, required=True)


class AdminOrderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEvent
        fields = '__all__'


class AdminOrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'cancel_reason', 'cancel_reason_note')


class AdminReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'


class AdminCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

    def create(self, validated_data):
        users = validated_data.pop('customers')
        coupon = Coupon.objects.create(**validated_data)
        coupon.customers.set(users)
        coupon.save()
        return coupon
