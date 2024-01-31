from rest_framework import serializers

from coreapp import roles
from notification.models import Notification


class NotificationAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'notification_type', 'recipient', 'message', 'is_read')

    def create(self, validated_data):
        recipient = validated_data.pop('recipient')
        notification = Notification.objects.create(**validated_data)
        notification.recipient.set(recipient)
        notification.save()
        return notification


class NotificationAdminListSerializer(serializers.ModelSerializer):
    sender_image = serializers.CharField(source='get_sender_image')
    name = serializers.CharField(source='get_sender_name')

    class Meta:
        model = Notification
        fields = ('id', 'created_at', 'sender_image', 'name', 'message')


class AdminNotificationIsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('is_read',)


class AdminFCMNotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    user_type = serializers.MultipleChoiceField(choices=roles.UserRoles.choices)
