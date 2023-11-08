from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ...models import CustomerInformation, Package, SubscriptionHistory
from . import serializers


class CustomerInformationAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = CustomerInformation.objects.all()
    serializer_class = serializers.CustomerInformationSerializer


class AdminPackageAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Package.objects.all()
    serializer_class = serializers.AdminPackageSerializer


class AdminSubscriptionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = SubscriptionHistory.objects.all()
    serializer_class = serializers.AdminSubscriptionSerializer
