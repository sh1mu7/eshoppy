from django_filters import rest_framework as dj_filters

from notification.models import Notification


class NotificationFilter(dj_filters.FilterSet):
    class Meta:
        model = Notification
        fields = ('is_read',)
