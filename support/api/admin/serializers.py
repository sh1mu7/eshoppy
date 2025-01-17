from rest_framework import serializers

from inventory.api.admin.serializers import AdminDocumentSerializer
from ...models import SupportTicket, TicketReply


class AdminSupportTicketListSerializer(serializers.ModelSerializer):
    attachment_url = AdminDocumentSerializer(source='attachment', many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = ('id', 'subject', 'description', 'status', 'priority', 'attachment_url')


class AdminTicketReplySerializer(serializers.ModelSerializer):
    attachment_url = AdminDocumentSerializer(source='attachment', many=True, read_only=True)

    class Meta:
        model = TicketReply
        fields = '__all__'

    def create(self, validated_data):
        attachment_data = validated_data.pop('attachment')
        ticket_reply = TicketReply.objects.create(**validated_data)
        ticket_reply.attachment.set(attachment_data)
        ticket_reply.save()
        return ticket_reply
