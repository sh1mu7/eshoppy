from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from django.db import transaction
from coreapp.models import User
from notification.api import filters
from notification.models import Notification
from . import serializers
import logging
from firebase_admin import messaging

logger = logging.getLogger(__name__)


class AdminNotificationAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationAdminSerializer
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.NotificationFilter

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @extend_schema(request=serializers.AdminNotificationIsReadSerializer)
    @action(detail=True, methods=['post'], url_path='markasread')
    def mark_as_read(self, request, pk):
        notification = Notification.objects.get(id=pk)
        serializer = serializers.AdminNotificationIsReadSerializer(data=request.data, instance=notification)
        serializer.is_valid(raise_exception=True)
        notification.is_read = True
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# this is required to bring the app foreground
class AdminFCMNotificationAPI(views.APIView):
    @extend_schema(
        request=serializers.AdminFCMNotificationSerializer
    )
    def post(self, request):
        serializer = serializers.AdminFCMNotificationSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data['title']
            message = serializer.validated_data['message']
            user_type = serializer.validated_data['user_type']

            tokens = User.objects.filter(role__in=user_type, fcm_token__isnull=False)

            notification = Notification.objects.create(title=title, message=message, notification_type=1,
                                                       sender=self.request.user)
            with transaction.atomic():
                for user in tokens:
                    notification.recipient.add(user.id)
            tokens = tokens.values_list('fcm_token', flat=True)
            push_notification(title, message, tokens.values_list('fcm_token', flat=True))
            return Response('Notification sent successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def push_notification(title, msg, tokens):
    """
    :param title: Title of notification
    :param msg: Message or body of notification
    :param tokens: Tokens of the users who will receive this notification
    :return:
    """
    chunks = [tokens[i:i + 500] for i in range(0, len(tokens), 500)]
    for chunk in chunks:
        messages = []
        for token in chunk:
            messages.append(
                messaging.Message(
                    notification=messaging.Notification(title, msg),
                    token=token
                )
            )
        response = messaging.send_each(messages)
        print(response)
