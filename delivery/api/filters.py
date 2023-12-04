from django_filters import rest_framework as filters
from delivery.models import DeliveryRequest, OrderDelivery


class RiderDeliveryRequestFilter(filters.FilterSet):
    class Meta:
        model = DeliveryRequest
        fields = ('order', 'is_accepted')


class RiderDeliveryStatus(filters.FilterSet):
    class Meta:
        model = OrderDelivery
        fields = ('rider_delivery_status',)



