from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from delivery.api.admin import serializers
from delivery.models import DeliveryRequest, DeliveryCharge
from sales import constants
from sales.models import Order, OrderEvent


class AdminOrderAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Order.objects.all()
    serializer_class = serializers.AdminOrderListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AdminOrderDetailSerializer
        return self.serializer_class

    @extend_schema(request=serializers.AdminOrderAssignRider)
    @action(detail=True, methods=['post'], url_path='assign_rider')
    def assign_order(self, request, pk=None):
        serializer = serializers.AdminOrderAssignRider(data=request.data)
        serializer.is_valid(raise_exception=True)
        rider_id = serializer.validated_data['rider_id']
        staff = self.request.user
        order = self.get_object()
        if order.order_stage == constants.OrderStage.DELIVERYMAN_ASSIGNED or order.order_status == constants.OrderStatus.CANCELED:
            return Response({'detail': [_('Already assigned a delivery rider or cancelled.')]},
                            status=status.HTTP_400_BAD_REQUEST)
        delivery_request = DeliveryRequest.objects.create(order_id=pk, staff=staff, rider_id=rider_id)
        order.order_stage = constants.OrderStage.DELIVERYMAN_ASSIGNED
        order.order_stage = constants.OrderStatus.PROCESSING
        order_event = OrderEvent.objects.create(
            order=order, event_status=constants.OrderEventStatus.DELIVERYMAN_ASSIGNED
        )
        delivery_request.save()
        order.save()
        order_event.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminDeliveryChargeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = serializers.AdminDeliveryChargeSerializer
    queryset = DeliveryCharge.objects.all()
