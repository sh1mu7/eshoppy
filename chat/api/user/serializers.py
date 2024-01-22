from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from chat.models import Message
from coreapp import roles
from coreapp.models import User


class UserMessageSerializer(serializers.ModelSerializer):
    receiver_name = serializers.CharField(source='get_receiver_name', read_only=True)
    sender_name = serializers.CharField(source='get_sender_name', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'receiver', 'receiver_name', 'sender', 'sender_name', 'content', 'attachment', 'timestamp')
        read_only_fields = ('timestamp', 'sender',)

    def validate(self, attrs):
        receiver = attrs.get('receiver')
        user = User.objects.get(id=receiver.id)
        if user and user.role == roles.UserRoles.ADMIN:
            return attrs
        else:
            raise serializers.ValidationError({'detail': _("Receivers must be a admin.")})

    def create(self, validated_data):
        user = self.context['request'].user
        attachment_data = validated_data.pop('attachment', None)
        message = Message.objects.create(sender=user, **validated_data)
        if attachment_data:
            message.attachment.set(attachment_data)
        message.save()
        return message
