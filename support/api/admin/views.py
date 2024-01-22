from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from ...models import SupportTicket, TicketReply
from .serializers import AdminSupportTicketListSerializer, AdminTicketReplySerializer


class AdminSupportTicketAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAdminUser, ]
    serializer_class = AdminSupportTicketListSerializer
    queryset = SupportTicket.objects.all()


class AdminTicketReplyAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = AdminTicketReplySerializer
    queryset = TicketReply.objects.all()
