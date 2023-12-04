from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from . import serializers
from ...models import SystemAlert, PersonalNotification


class AdminSystemAlertAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = SystemAlert.objects.all()
    serializer_class = serializers.AdminSystemAlertSerializer


class AdminPersonalNotificationAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = PersonalNotification.objects.all()
    serializer_class = serializers.AdminPersonalNotificationSerializer
