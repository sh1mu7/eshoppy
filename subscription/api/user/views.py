from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from coreapp.permissions import IsCustomer
from ...models import CustomerInformation, Package, SubscriptionHistory
from . import serializers


class UserPackageAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Package.objects.all()
    serializer_class = serializers.UserPackageSerializer


class UserSubscriptionAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = SubscriptionHistory.objects.all()
    serializer_class = serializers.UserSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = SubscriptionHistory.objects.filter(customer=user, is_expired=False)
        return queryset
