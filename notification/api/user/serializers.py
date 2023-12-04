from rest_framework import serializers
from ...models import SystemAlert, PersonalNotification


class UserSystemAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAlert
        fields = ('id', 'title', 'message', 'is_read')


class UserPersonalNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalNotification
        fields = ('id', 'title', 'message', 'timestamp', 'is_read')


class IsReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField(default=True)
