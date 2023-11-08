from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ...models import Package, SubscriptionHistory


class UserPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionHistory
        fields = ('id', 'package')

    def validate(self, attrs):
        user = self.context['request'].user
        if SubscriptionHistory.objects.filter(customer=user, is_expired=False).exists():
            raise serializers.ValidationError({'detail': [_('You already have a active package.')]})
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        subscription = SubscriptionHistory.objects.create(**validated_data, customer=user)
        return subscription
