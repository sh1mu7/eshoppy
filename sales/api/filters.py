from django_filters import rest_framework as dj_filters

from sales.models import Order


# Done : Is active filter needed for everything
class OrderFilter(dj_filters.FilterSet):
    name = dj_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ('order_status',)
