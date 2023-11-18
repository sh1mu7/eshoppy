from django_filters import rest_framework as filters
from delivery.models import DeliveryRequest


class RiderDeliveryRequestFilter(filters.FilterSet):
    class Meta:
        model = DeliveryRequest
        fields = ('order', 'is_accepted')
