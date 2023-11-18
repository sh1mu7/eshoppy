from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from django_filters import rest_framework as dj_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from coreapp.permissions import IsDeliveryStaff
from delivery.models import DeliveryRider, DeliveryRequest, OrderDelivery
from . import serializers
from .. import filters


class RiderProfileAPI(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    permission_classes = [IsDeliveryStaff, ]
    queryset = DeliveryRider.objects.all()
    serializer_class = serializers.DeliveryRiderDocumentsSerializer


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
    def delivery_request_accept_or_reject(self, request, pk=None):
        delivery_request = self.get_object()
        serializer = serializers.DeliveryRequestAcceptOrRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_accepted = serializer.validated_data['is_accepted']
        rider = self.request.user
        order = delivery_request.order
        print(delivery_request)
        if is_accepted:
            delivery_request.is_accepted = True
            order_delivery = OrderDelivery.objects.create(
                delivery_request=delivery_request, order=order, customer=order.customer, rider=rider,
                estd_delivery_time="2023-11-17T06:43:24.877Z", address='dd'
            )
            delivery_request.save()
            order_delivery.save()
            return Response({'detail': [_('Accepted by rider')]}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': [_('Cancelled by rider')]}, status=status.HTTP_400_BAD_REQUEST)
