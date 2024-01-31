from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response

from coreapp.permissions import IsCustomer
from notification.api import filters
from notification.models import Notification
from . import serializers


class UserNotificationAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Notification.objects.all()
    serializer_class = serializers.UserNotificationSerializer
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.NotificationFilter

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @extend_schema(request=serializers.UserNotificationMarkAsReadSerializer)
    @action(detail=True, methods=['post'], url_path='markasread')
    def mark_as_read(self, request, pk):
        notification = Notification.objects.get(id=pk)
        serializer = serializers.UserNotificationMarkAsReadSerializer(data=request.data, instance=notification)
        serializer.is_valid(raise_exception=True)
        notification.is_read = True
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='markallasread')
    def mark_all_as_read(self, request):
        notification = Notification.objects.filter(recipient=self.request.user)
        for obj in notification:
            obj.is_read = True
            obj.save()
        return Response({'details': 'All notifications are marked as read.'}, status=status.HTTP_200_OK)
