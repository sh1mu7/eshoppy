from rest_framework import serializers

from delivery.models import DeliveryCharge


class AdminDeliveryChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = ('km_distance', 'amount', 'is_active')


