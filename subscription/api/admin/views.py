from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser

from coreapp.models import User
from coreapp.permissions import IsCustomer
from ...models import Package, SubscriptionHistory
from . import serializers


class CustomerInformationAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = User.objects.filter(role=2).all()
    serializer_class = serializers.CustomerInformationSerializer
    # Todo : Need to modify as per UI


class AdminPackageAPI(viewsets.ModelViewSet):
    permission_classes = [IsCustomer, ]
    queryset = Package.objects.all()
    serializer_class = serializers.AdminPackageSerializer


class AdminSubscriptionAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = SubscriptionHistory.objects.all()
    serializer_class = serializers.AdminSubscriptionSerializer
