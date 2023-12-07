from rest_framework.viewsets import ModelViewSet
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
from subscription.models import SubscriptionHistory
from . import serializers
from ...models import Reason, Coupon


class AdminOrderAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Order.objects.all()
    serializer_class = serializers.AdminOrderListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AdminOrderDetailSerializer
        return self.serializer_class

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='cancel/accept')
    def cancel_accept(self, request, pk=None):
        order_staff = self.request.user
        order = self.get_object()
        if order.order_status == constants.OrderStatus.CANCELED or order.has_cancel_request:
            return Response({'detail: Order already has been canceled.'}, status=status.HTTP_400_BAD_REQUEST)
        order.order_status = constants.OrderStatus.CANCELED
        order.cancel_status = constants.OrderCancelStatus.ACCEPT
        order.has_cancel_request = False

        for item in order.orderitem_set.all():
            item.product.quantity += item.quantity
            item.product.save()
        order.order_staff = order_staff
        order.save()
        return Response({'detail': 'Order cancel request has been rejected.'}, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='cancel/reject')
    def cancel_reject(self, request, pk=None):
        order_staff = self.request.user
        order = self.get_object()
        if order.order_status == constants.OrderStatus.CANCELED or order.has_cancel_request:
            return Response({'detail: Order already has been canceled.'}, status=status.HTTP_400_BAD_REQUEST)
        if order.has_cancel_request:
            order.order_status = constants.OrderStatus.PROCESSING
            order.cancel_status = constants.OrderCancelStatus.REJECT
        order.order_staff = order_staff
        order.save()
        return Response({'detail': 'Order has been canceled.'}, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.AdminOrderAssignRider)
    @action(detail=True, methods=['post'], url_path='assign_rider')
    def assign_rider(self, request, pk=None):
        serializer = serializers.AdminOrderAssignRider(data=request.data)
        serializer.is_valid(raise_exception=True)
        rider_id = serializer.validated_data['rider_id']
        staff = self.request.user
        order = self.get_object()
        if order.order_stage == constants.OrderStage.DELIVERYMAN_ASSIGNED or order.order_status == constants.OrderStatus.CANCELED:
            return Response({'detail': [_('Already assigned a delivery rider or cancelled.')]},
                            status=status.HTTP_400_BAD_REQUEST)
        delivery_request = DeliveryRequest.objects.create(order_id=pk, staff=staff, rider_id=rider_id)
        order.order_status = constants.OrderStatus.PROCESSING
        order.order_stage = constants.OrderStage.DELIVERYMAN_ASSIGNED
        order_event = OrderEvent.objects.create(
            order=order, event_status=constants.OrderEventStatus.DELIVERYMAN_ASSIGNED)
        delivery_request.save()
        order.save()
        order_event.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.AdminOrderChangePaymentStatus)
    @action(detail=True, methods=['post'], url_path='change_payment_status')
    def change_payment_status(self, request):
        order = self.get_object()
        serializer = serializers.AdminOrderChangePaymentStatus(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_status = serializer.validated_data['payment_status']
        order.payment_status = payment_status
        order.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.AdminOrderStatusChangeSerializer)
    @action(detail=True, methods=['post'], url_path='process')
    def process(self, request):
        order = self.get_object()
        serializer = serializers.AdminOrderStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_status = serializer.validated_data['order_status']
        order.order_status = order_status
        order.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminReasonAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Reason.objects.all()
    serializer_class = serializers.AdminReasonSerializer


class AdminCouponAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Coupon.objects.all()
    serializer_class = serializers.AdminCouponSerializer
