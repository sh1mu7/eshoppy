from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from coreapp import roles
from coreapp.models import User
from sales.api.admin.serializers import AdminOrderItemSerializer
from sales.models import OrderEvent, Order


class AdminOrderListSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='get_item_count', read_only=True)
    customer_name = serializers.CharField(source='get_customer_name')
    customer_mobile = serializers.CharField(source='get_customer_mobile')

    class Meta:
        model = Order
        fields = ('created_at', 'id', 'invoice_no', 'customer_name', 'customer_mobile', 'item_count', 'order_status',
                  'delivery_status', 'total')


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_customer_name')
    customer_mobile = serializers.CharField(source='get_customer_mobile')
    order_items = AdminOrderItemSerializer(many=True, read_only=True, source='get_order_item')
    order_event_status = serializers.CharField(source='get_order_event_status')

    class Meta:
        model = Order
        fields = (
            "id", 'invoice_no', 'customer_mobile', 'order_items', 'customer_name', 'order_event_status', 'subtotal',
            'vat', 'shipping_charge', 'customer_note', 'payment_method', 'discount', 'total', 'shipping_address',
            'created_at', 'coupon', 'customer'
        )


class AdminOrderAssignRider(serializers.Serializer):
    rider_id = serializers.IntegerField(allow_null=False, required=True)

    def validate(self, attrs):
        rider_id = attrs.get('rider_id')

        if rider_id and not User.objects.filter(id=rider_id, role=roles.UserRoles.DELIVERY_STAFF).exists():
            raise serializers.ValidationError({'user_id': [_('Invalid user id')]})


class AdminOrderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderEvent
        fields = '__all__'


class AdminOrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'cancel_reason', 'cancel_reason_note')
