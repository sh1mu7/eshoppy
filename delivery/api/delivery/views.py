from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from coreapp.permissions import IsDeliveryStaff
from delivery.models import DeliveryRider, DeliveryRequest, OrderDelivery
from delivery import constants
from sales import constants as sale_const
from sales.models import OrderEvent
from . import serializers
from .. import filters


class DeliveryManProfileAPI(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    permission_classes = [IsDeliveryStaff]
    queryset = DeliveryRider.objects.all()
    serializer_class = serializers.DeliveryRiderProfileCreateSerializer

    def get_queryset(self):
        queryset = DeliveryRider.objects.order_by('-created_at').all()[:1]
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RiderProfileListSerializer
        return self.serializer_class


class RiderDeliveryRequestAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsDeliveryStaff, ]
    queryset = DeliveryRequest.objects.all()
    serializer_class = serializers.RiderDeliveryRequestListSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.RiderDeliveryRequestFilter

    def get_queryset(self):
        rider = self.request.user
        queryset = DeliveryRequest.objects.filter(rider=rider)
        return queryset

    @extend_schema(request=serializers.DeliveryRequestAcceptOrRejectSerializer)
    @action(detail=True, methods=['post'], url_name='accept_or_reject')
    def accept_or_reject(self, request, pk=None):
        delivery_request = self.get_object()
        serializer = serializers.DeliveryRequestAcceptOrRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if delivery_request.is_accepted:
            return Response({'detail': [_('Request has already been accepted.')]}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.DeliveryRequestAcceptOrRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_accepted = serializer.validated_data['is_accepted']
        rider = self.request.user
        order = delivery_request.order
        if is_accepted:
            order.delivery_staff = rider
            delivery_request.is_accepted = True
            order_delivery = OrderDelivery.objects.create(
                delivery_request=delivery_request, order=order, customer=order.customer, rider=rider,
                estd_delivery_time=order.estd_delivery_time,
                rider_delivery_status=constants.RiderOrderDeliveryStatus.ACTIVE,
                address=order.shipping_address, latitude=order.customer_latitude, longitude=order.customer_longitude
            )
            order.save()
            delivery_request.save()
            order_delivery.save()
            return Response({'detail': [_('Accepted by rider')]}, status=status.HTTP_200_OK)
        return Response({'detail': [_('Cancelled by rider')]}, status=status.HTTP_400_BAD_REQUEST)


class RiderOrderDeliveryAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsDeliveryStaff, ]
    queryset = OrderDelivery.objects.all()
    serializer_class = serializers.RiderOrderDeliverySerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.RiderDeliveryStatus

    def get_queryset(self):
        user = self.request.user
        queryset = OrderDelivery.objects.filter(rider=user)
        return queryset

    @extend_schema(request=serializers.RiderStatusChangeSerializer)
    @action(detail=True, methods=['post'], url_path='status_change')
    def status_change(self, request, pk=None):
        order_delivery = self.get_object()
        order_event = OrderEvent.objects.all()

        serializer = serializers.RiderStatusChangeSerializer(data=request.data)
        if serializer.is_valid():
            rider_delivery_status = serializer.validated_data['rider_delivery_status']
            order_delivery.rider_delivery_status = rider_delivery_status
            if rider_delivery_status == constants.RiderOrderDeliveryStatus.COMPLETED:
                order_delivery.order.order_status = sale_const.OrderStatus.DELIVERED
                order_delivery.order.order_stage = sale_const.OrderStage.DELIVERED
                order_delivery.status = sale_const.DeliveryStatus.DELIVERED
                order_event.create(order=order_delivery.order, event_status=sale_const.OrderEventStatus.DELIVERED)
            order_delivery.save()
            return Response({'detail': 'Delivery is completed'})
