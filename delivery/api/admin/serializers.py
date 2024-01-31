from rest_framework import serializers

from coreapp.models import User
from delivery.models import DeliveryCharge, DeliveryRider


class AdminDeliveryChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = ('id', 'km_distance', 'amount', 'is_active')


class AdminDeliveryRiderList(serializers.ModelSerializer):
    # image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = DeliveryRider
        fields = '__all__'
