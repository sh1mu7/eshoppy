from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from coreapp.permissions import IsCustomer
from utility import constants as payment_constant
from coreapp import constants
from coreapp.utils.auth_utils import get_client_info
from utility.models import Payment
from utility.utils.payment_utils import generate_bill_url
from ...models import Package, SubscriptionHistory
from . import serializers


class UserPackageAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Package.objects.all()
    serializer_class = serializers.UserPackageSerializer


class UserSubscriptionAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = SubscriptionHistory.objects.all()
    serializer_class = serializers.UserSubscriptionCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserSubscriptionCreateSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    user = self.request.user
                    if SubscriptionHistory.objects.filter(customer=user, is_expired=False).exists():
                        return Response({
                            'detail': _("You already have an active subscription.")
                        }, status=status.HTTP_400_BAD_REQUEST)

                    package = Package.objects.get(id=serializer.validated_data['package'])
                    now = datetime.now()
                    expiry_date = now + relativedelta(months=package.duration)
                    expiry_date = expiry_date.date()
                    subscription = SubscriptionHistory.objects.create(
                        customer=user, package=package, membership_type=package.package_type, start_date=now,
                        expiry_date=expiry_date, amount=package.price)
                    subscription.save()
                    user.membership_type = subscription.membership_type
                    user.save()
                    payment_method = serializer.validated_data['payment_method']
                    ip, user_agent = get_client_info(request)
                    payment = Payment.objects.create(amount=subscription.amount, ip_address=ip,
                                                     transaction_type=payment_constant.TransactionType.SUBSCRIPTION,
                                                     subscription=subscription,
                                                     status=payment_constant.PaymentStatus.PENDING,
                                                     payment_method=payment_method, user=user)
                    payment.save()
                    data = serializers.UserSubscriptionListSerializer(subscription).data
                    # if not payment_method == payment_constant.PaymentMethod.CASH:
                    #     bill_url = generate_bill_url(payment)
                    #     if not bill_url:
                    #         return Response({'detail': 'Bill url not created.'}, status=status.HTTP_400_BAD_REQUEST)
                    #     data['bill_url'] = bill_url

                    return Response(data=data, status=status.HTTP_200_OK)
            except Exception as e:
                transaction.set_rollback(True)
                return Response({'detail': f'{str(e)} can not buy subscription. Please try again.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Serializer is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        queryset = SubscriptionHistory.objects.filter(customer=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserSubscriptionListSerializer
        return self.serializer_class
