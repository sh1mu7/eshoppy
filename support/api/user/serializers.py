from rest_framework import serializers
from ...models import SupportTicket


class UserSupportTicketSerializer(serializers.ModelSerializer):
    attachment_url = serializers.CharField(source='attachment.get_url', read_only=True)

    class Meta:
        model = SupportTicket
        fields = ('id', 'subject', 'description', 'status', 'priority', 'attachment', 'attachment_url')

    def create(self, validated_data):
        user = self.context['request'].user
        attachment_data = validated_data.pop('attachment')
        support_ticket = SupportTicket.objects.create(user=user, **validated_data)
        support_ticket.attachment.set(attachment_data)
        support_ticket.save()
        return support_ticket
