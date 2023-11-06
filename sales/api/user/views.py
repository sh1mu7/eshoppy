from rest_framework import viewsets, mixins
from coreapp.models import Address
from coreapp.permissions import IsCustomer
from sales.models import Reason, Coupon
from .serializers import CustomerAddressSerializer, CustomerReasonSerializer, CustomerCouponSerializer


class CustomerAddressAPI(viewsets.ModelViewSet):
    permission_classes = [IsCustomer, ]
    queryset = Address.objects.all()
    serializer_class = CustomerAddressSerializer


class CustomerReasonAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Reason.objects.all()
    serializer_class = CustomerReasonSerializer


class CustomerCouponAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Coupon.objects.all()
    serializer_class = CustomerCouponSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = Coupon.objects.filter(customers=user)
        return queryset
