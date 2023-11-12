from rest_framework import serializers
from cart.models import Cart
from coreapp.models import Address
from ...models import Reason, Coupon


class UserCheckOutSerializer(serializers.Serializer):
    cart_items = serializers.ListField(allow_empty=False, allow_null=False)
    coupon_code = serializers.CharField(allow_null=True, required=False)
    address = serializers.IntegerField()
    payment_method = serializers.IntegerField()

    def validate(self, attrs):
        user = self.context['request'].user
        cart_items = Cart.objects.filter(id__in=list(attrs['cart_items']), user=user)
        if not cart_items and len(cart_items) < 1:
            raise serializers.ValidationError({'cart_items': ['cart items not found']})
        return attrs


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Address.objects.create(**validated_data, user=user)


class CustomerCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'coupon_title', 'coupon_code', 'discount_type', 'discount_amount', 'expire_date', 'is_active')


class CustomerReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('reason_type', 'reason_name')
