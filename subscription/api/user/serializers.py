from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from ... import constants
from ...models import Package, SubscriptionHistory


class UserPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class UserSubscriptionCreateSerializer(serializers.Serializer):
    package = serializers.IntegerField()
    payment_method = serializers.IntegerField()

    def validate(self, attrs):
        package = attrs['package']
        if not Package.objects.filter(id=package, is_active=True).exists():
            raise serializers.ValidationError({'package': [_("Invalid package id")]})
        return attrs

    def create(self, validated_data):
        package = validated_data['package']
        subscription = SubscriptionHistory.objects.create(
            package=package, amount=package.price, membership_type=package.package_type)
        subscription.save()
        return subscription


class UserSubscriptionListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='get_package_name', read_only=True)
    price = serializers.CharField(source='get_package_price', read_only=True)
    details = serializers.CharField(source='get_package_details', read_only=True)
    package_expired = serializers.CharField(source='get_is_expired', read_only=True)

    class Meta:
        model = SubscriptionHistory
        fields = ('package_name', 'price', 'details', 'start_date', 'expiry_date', 'package_expired')
