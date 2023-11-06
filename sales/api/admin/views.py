from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .serializers import AdminReasonSerializer, AdminCouponSerializer
from ...models import Reason, Coupon


class AdminReasonAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Reason.objects.all()
    serializer_class = AdminReasonSerializer


class AdminCouponAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Coupon.objects.all()
    serializer_class = AdminCouponSerializer
