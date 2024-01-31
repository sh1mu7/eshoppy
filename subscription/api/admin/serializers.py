from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from coreapp import roles
from coreapp.models import User
from ...models import Package, SubscriptionHistory


class CustomerInformationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'mobile', 'fcm_token', 'customer_name')
        # Todo : Need to fix


class AdminPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class AdminSubscriptionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_customer_name', read_only=True)
    package_name = serializers.CharField(source='get_package_name', read_only=True)

    class Meta:
        model = SubscriptionHistory
        fields = ('package', 'customer', 'expiry_date', 'customer_name', 'package_name')

    def validate(self, attrs):
        customer = attrs.get('customer')
        if not User.objects.filter(id=customer.id, role=roles.UserRoles.CUSTOMER).exists():
            raise serializers.ValidationError({'detail': [_('user is not customer')]})
        return attrs

    def create(self, validated_data):
        package = validated_data.get('package')
        return SubscriptionHistory.objects.create(amount=package.price, membership_type=package.package_type,
                                                  **validated_data)
