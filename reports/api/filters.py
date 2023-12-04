from django_filters import rest_framework as filters
from delivery.models import OrderDelivery


class DeliveryReportFilter(filters.FilterSet):
    class Meta:
        model = OrderDelivery
        fields = ('created_at', 'id')
