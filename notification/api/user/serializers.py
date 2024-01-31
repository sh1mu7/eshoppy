from rest_framework import serializers

from notification.models import Notification


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'message', 'is_read', 'created_at')


class UserNotificationMarkAsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'is_read')


# class UserNotificationMarkAllAsReadSerializer(serializers.ModelSerializer):
#     class Meta: