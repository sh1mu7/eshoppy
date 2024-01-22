from coreapp.permissions import IsCustomer
from .. import filters
from ...models import Message
from .serializers import UserMessageSerializer
from rest_framework import viewsets, mixins
from django_filters import rest_framework as dj_filters


class UserMessageAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer]
    serializer_class = UserMessageSerializer
    queryset = Message.objects.all()
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.UserMessageFilter

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user)
