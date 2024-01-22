from django_filters import rest_framework as dj_filters

from chat.models import Message


# Done : Is active filter needed for everything
class UserMessageFilter(dj_filters.FilterSet):
    class Meta:
        model = Message
        fields = ('sender',)

