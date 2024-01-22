from rest_framework.permissions import IsAdminUser
from ...models import Message
from .serializers import AdminMessageSerializer
from rest_framework import viewsets


class AdminMessageAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = AdminMessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
