from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from coreapp.permissions import IsDeliveryStaff
from coreapp.utils.twilio_utils import send_otp_via_sms
from delivery.models import DeliveryRider, DeliveryRequest, OrderDelivery, RiderCommission
from delivery import constants
from sales import constants as sale_const
from sales.models import OrderEvent
from utility.models import Refund, Payment
from . import serializers
from .. import filters
from ...constants import CommissionStatus
from ...utils.commission_utils import get_commission_amount
from ...utils.otp_utils import generate_otp


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
                estd_delivery_time=order.estd_delivery_time, status=sale_const.DeliveryStatus.PENDING,
                address=order.shipping_address, latitude=order.customer_latitude, longitude=order.customer_longitude
            )
            order.save()
            delivery_request.save()
            order_delivery.save()
            return Response({'detail': [_('Accepted by rider')]}, status=status.HTTP_200_OK)
        else:
            order.delivery_staff = rider
            delivery_request.is_accepted = True
            order_delivery = OrderDelivery.objects.create(
                delivery_request=delivery_request, order=order, customer=order.customer, rider=None,
                estd_delivery_time=order.estd_delivery_time, status=sale_const.DeliveryStatus.CANCELED,
                address=order.shipping_address, latitude=order.customer_latitude, longitude=order.customer_longitude
            )
            order.save()
            delivery_request.save()
            order_delivery.save()
            return Response({'detail': [_('Cancelled by rider')]}, status=status.HTTP_200_OK)


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

    @extend_schema(request=None)
    @action(detail=True, methods=['get'], url_path='send_otp')
    def send_otp(self, request, pk=None):
        order_delivery = self.get_object()
        otp = generate_otp()
        order_delivery.otp = otp
        # send_otp_via_sms(order_delivery.customer.mobile,otp)
        # TODO: Need to remove comment and active twilio service
        order_delivery.save()
        return Response(status=status.HTTP_200_OK)

    @extend_schema(request=serializers.RiderVerifyOTPSerializer)
    @action(detail=True, methods=['post'], url_path='verify_otp')
    def verify_otp(self, request, pk=None):
        order_delivery = self.get_object()
        serializer = serializers.RiderVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        if otp != order_delivery.otp:
            return Response({'detail': 'OTP is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        order_delivery.is_verified = True
        order_delivery.save()
        return Response({'detail': 'Order verified successfully.'})

    @extend_schema(request=serializers.RiderLiverTrackSerializer)
    @action(detail=True, methods=['post'], url_path='live-track')
    def live_track_rider(self, request, pk=None):
        order_delivery = self.get_object()
        serializer = serializers.RiderLiverTrackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        longitude = serializer.validated_data['longitude']
        latitude = serializer.validated_data['latitude']
        order_delivery.longitude = longitude
        order_delivery.latitude = latitude
        order_delivery.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='mark_as_complete')
    def mark_as_complete(self, request, pk=None):
        order_delivery = self.get_object()
        user = self.request.user
        if not order_delivery.is_verified:
            return Response({'detail': 'Order is not verified'}, status=status.HTTP_400_BAD_REQUEST)
        if order_delivery.order:
            order_delivery.order.order_stage = sale_const.OrderStage.DELIVERED
            order_delivery.order.order_status = sale_const.OrderStatus.DELIVERED
            order_delivery.status = sale_const.DeliveryStatus.COMPLETED
            commission_amount = get_commission_amount(order_delivery.order.total)
            rider_commission = RiderCommission.objects.create(
                rider=user, amount=commission_amount, order=order_delivery.order,
                commission_status=CommissionStatus.PENDING
            )
            rider_commission.save()
            order_delivery.save()
            return Response({'detail': 'Successfully delivered'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Delivery failed'}, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='mark_as_returned')
    def mark_as_returned(self, request, pk=None):
        order_delivery = self.get_object()
        if not order_delivery.is_verified:
            return Response({'detail': 'Order is not verified'}, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.get(order=order_delivery.order)
        payment_amount = payment.amount
        if order_delivery.order and order_delivery.is_verified:
            order_delivery.order.order_stage = sale_const.OrderStage.REQUEST_SENT
            order_delivery.order.order_status = sale_const.OrderStatus.PROCESSING
            order_delivery.status = sale_const.DeliveryStatus.RETURNED
            refund = Refund.objects.create(
                order=order_delivery.order, customer_id=order_delivery.order.customer,
                payment=payment, user_type=order_delivery.order.customer.roles,
                refundable_amount=payment_amount, is_refunded=False
            )
            refund.save()
            order_delivery.save()
            return Response({'detail': 'Successfully Returned'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Return failed'}, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.RiderStatusChangeSerializer)
    @action(detail=True, methods=['post'], url_path='process')
    def process(self, request, pk=None):
        order_delivery = self.get_object()
        serializer = serializers.RiderStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['rider_delivery_status'] == 2:
            order_delivery.status = serializer.validated_data['rider_delivery_status']
            order_delivery.save()
            return Response({'detail': 'Order picked successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
