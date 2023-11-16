from rest_framework import viewsets, mixins
from coreapp.permissions import IsDeliveryStaff
from delivery.models import DeliveryRider
from . import serializers


class RiderProfileAPI(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    permission_classes = [IsDeliveryStaff, ]
    queryset = DeliveryRider.objects.all()
    serializer_class = serializers.DeliveryRiderDocumentsSerializer
