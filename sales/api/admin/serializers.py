from rest_framework import serializers

from ...models import Reason, Coupon


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
