from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from delivery.api.admin import serializers
from delivery.models import DeliveryRequest, DeliveryCharge, DeliveryRider
from sales import constants
from sales.models import Order, OrderEvent


class AdminDeliveryChargeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = serializers.AdminDeliveryChargeSerializer
    queryset = DeliveryCharge.objects.all()


class AdminDeliveryRiderAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = serializers.AdminDeliveryRiderList
    queryset = DeliveryRider.objects.all()
