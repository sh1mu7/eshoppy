from rest_framework import viewsets, mixins
from .serializers import UserSupportTicketSerializer
from coreapp.permissions import IsCustomer
from ...models import SupportTicket


class UserSupportTicketAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer]
    serializer_class = UserSupportTicketSerializer
    queryset = SupportTicket.objects.all()

    def get_queryset(self):
        user = self.request.user
        return SupportTicket.objects.filter(user=user)
