from rest_framework import serializers

from coreapp.models import Address
from ...models import Reason, Coupon


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
