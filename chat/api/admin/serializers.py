from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from chat.models import Message
from coreapp import roles
from coreapp.models import User, Document
from inventory.api.admin.serializers import AdminDocumentSerializer


class AdminMessageSerializer(serializers.ModelSerializer):
    receiver_name = serializers.CharField(source='get_receiver_name', read_only=True)
    attachment = serializers.PrimaryKeyRelatedField(many=True, queryset=Document.objects.all(), required=False)

    class Meta:
        model = Message
        fields = ('id', 'receiver', 'receiver_name', 'content', 'timestamp', 'attachment',)
        read_only_fields = ('timestamp',)

    def validate(self, attrs):
        receiver = attrs.get('receiver')
        user = User.objects.get(id=receiver.id)
        if user and user.role == roles.UserRoles.CUSTOMER:
            return attrs
        else:
            raise serializers.ValidationError({'detail': _("Receivers must be a customer.")})

    def create(self, validated_data):
        user = self.context['request'].user
        attachment_data = validated_data.pop('attachment', None)
        print(attachment_data)
        message = Message.objects.create(sender=user, **validated_data)
        if attachment_data:
            message.attachment.set(attachment_data)
            message.save()
        message.save()
        return message


class AdminMessageListSerializer(AdminMessageSerializer):
    receiver_name = serializers.CharField(source='get_receiver_name', read_only=True)
    attachment = AdminDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = (
            'id', 'receiver', 'receiver_name', 'content', 'timestamp', 'attachment', 'created_at', 'updated_at',
            'sender'
        )
        read_only_fields = ('attachment',)
