from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from delivery.api.admin import serializers
from sales.models import Order


class AdminOrderAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Order.objects.all()
    serializer_class = serializers.AdminOrderListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AdminOrderDetailSerializer
        return self.serializer_class
