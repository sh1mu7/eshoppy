from rest_framework import serializers
from ...models import Reason, Coupon, OrderItem, Order


class AdminOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem.objects.all()
        fields = ('id', 'product', 'product_name', 'quantity', 'price', 'subtotal')


class AdminOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_customer_name', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'invoice_no', 'customer_name', 'total', 'order_status', 'has_cancel_request')


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
