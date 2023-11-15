from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from coreapp import roles
from coreapp.models import User
from ...models import Package, SubscriptionHistory


class CustomerInformationSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'mobile', 'device_id', 'customer_name')
        # Todo : Need to fix


class AdminPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class AdminSubscriptionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = SubscriptionHistory
        fields = '__all__'

    def validate(self, attrs):
        customer = attrs.get('customer')
        if not User.objects.filter(user=customer, role=roles.UserRoles.CUSTOMER).exists():
            raise serializers.ValidationError({'detail': [_('user is not customer')]})
