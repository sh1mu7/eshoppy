from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from cart.api.user.serializers import CartPriceCalculationSerializer, OrderPriceCalculationSerializer
from cart.models import Cart
from coreapp.models import Address
from coreapp.permissions import IsCustomer
from coreapp.utils.auth_utils import get_client_info
from delivery.models import OrderDelivery
from delivery.utils.distance_utils import haversine
from inventory.models import Product, ProductVariant
from sales.models import Reason, Coupon, Order, OrderItem, OrderEvent
from utility.models import Payment
from utility.utils.payment_utils import generate_bill_url
from . import serializers
from ... import constants
from utility import constants as payment_constants
from ...constants import OrderEventStatus
from ...utils import coupon_utils
from ...utils.process_order_utils import process_cart_and_coupon, adjust_estd_delivery_time, shipping_charge_calculate, \
    CouponNotFoundError


class CustomerCheckoutAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Order.objects.all()
    serializer_class = serializers.UserCheckOutSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                if 'coupon_code' in serializer.validated_data:
                    coupon_code = serializer.validated_data['coupon_code']
                else:
                    coupon_code = None
                address_id = serializer.data['address']
                coupon_code = serializer.data['coupon_code']
                payment_method = serializer.data['payment_method']
                cart_items_id = serializer.data['cart_items']
                cart_items = Cart.objects.filter(user=self.request.user, id__in=cart_items_id)
                address = Address.objects.get(id=address_id)
                customer = self.request.user
                vat_amount = 0
                shipping_charge = 0
                total = 0
                subtotal = 0
                discount = 0

                order = Order.objects.create(
                    customer=customer, customer_email=customer.email, customer_phone=customer.mobile,
                    customer_name=customer.get_full_name, customer_latitude=address.latitude,
                    customer_longitude=address.longitude, shipping_address=address, payment_method=payment_method)
                subtotal, vat_amount, discount = process_cart_and_coupon(customer, subtotal, vat_amount, order,
                                                                         cart_items_id, coupon_code)
                estimated_delivery_time = adjust_estd_delivery_time(order)
                dd = shipping_charge_calculate(order.customer_latitude, order.customer_longitude)
                order.subtotal = subtotal
                order.vat = vat_amount
                order.shipping_charge = dd
                total += subtotal + vat_amount + shipping_charge - discount
                order.discount = discount
                order.total = total
                order.estd_delivery_time = estimated_delivery_time
                order.order_stage = constants.OrderStage.REQUEST_SENT
                order.save()
                order.refresh_from_db()
                # TODO: Need to remove the comment
                cart_items.delete()
                OrderEvent.objects.create(order=order, event_status=constants.OrderEventStatus.ORDER_PLACED,
                                          note='Order has been placed successfully').save()
                ip, user_agent = get_client_info(request)

                payment = Payment.objects.create(
                    amount=total, ip_address=ip, order=order, status=payment_constants.PaymentStatus.PENDING,
                    transaction_type=payment_constants.TransactionType.ORDER, payment_method=payment_method,
                    user=self.request.user).save()
                if not payment_method == payment_constants.PaymentMethod.CASH:
                    bill_url = generate_bill_url(payment)
                    if not bill_url:
                        return Response({'detail': 'Bill Url.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    bill_url = None
                # TODO: Need to setup the payment configuration
                data = {
                    'detail': 'Order has been placed successfully.',
                    'bill_url': bill_url,
                    'tracking_id': order.invoice_no,
                    'order_id': order.id
                }

                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'detail': [_(f"{str(e)} can not create order. Try again.")]},
                            status=status.HTTP_400_BAD_REQUEST)


class CustomerOrderAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Order.objects.all()
    serializer_class = serializers.CustomerOrderListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CustomerOrderDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(customer=user)
        return queryset

    @extend_schema(request=serializers.CustomerOrderCancelSerializer)
    @action(detail=True, methods=['post'], url_name='cancel_with_reason')
    def cancel_with_reason(self, request, pk=None):
        order = self.get_object()
        serializer = serializers.CustomerOrderCancelSerializer(data=request.data, instance=order)
        serializer.is_valid(raise_exception=True)
        cancel_reason = serializer.validated_data['cancel_reason']
        cancel_reason_note = serializer.validated_data['cancel_reason_note']
        if order.order_status == constants.OrderStatus.CANCELED:
            return Response({'detail': 'Order has been already canceled'}, status=status.HTTP_400_BAD_REQUEST)
        order.has_cancel_request = True
        order.cancel_status = constants.OrderCancelStatus.PENDING
        order.cancel_reason = cancel_reason
        order.cancel_reason_note = cancel_reason_note
        for item in order.orderitem_set.all():
            item.product.quantity += item.quantity
            item.product.save()
        order.save()
        order_events = OrderEvent.objects.create(order=order, event_status=constants.OrderEventStatus.REQUEST_SENT,
                                                 note=cancel_reason_note)
        order_events.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_without_reason(self, request, pk=None):
        order = self.get_object()
        if order.order_status == constants.OrderStatus.CANCELED:
            return Response({'detail: Order already has been canceled.'}, status=status.HTTP_400_BAD_REQUEST)
        order.order_status = constants.OrderStatus.CANCELED
        for item in order.orderitem_set.all():
            item.product.quantity += item.quantity
            item.product.save()
        order.save()
        return Response({'detail': 'Order has been canceled.'}, status=status.HTTP_200_OK)

    @extend_schema(request=OrderPriceCalculationSerializer)
    @action(detail=False, methods=['post'], url_path='calculate_price')
    def order_price_calculation(self, request):
        serializer = OrderPriceCalculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.data['order_id']
        order = Order.objects.get(invoice_no=order_id)
        subtotal = order.subtotal
        vat = order.vat
        discount = order.discount
        total = order.total
        response_data = {
            'subtotal': subtotal,
            'vat': vat,
            'discount': discount,
            'total': total,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: serializers.CustomerOrderTrackSerializer})
    @action(detail=False, methods=['get'], url_path='(?P<tracking_id>[^/.]+)/track')
    def track_order(self, request, tracking_id=None):
        try:
            order = Order.objects.get(invoice_no=tracking_id, customer=self.request.user)
            serializer = serializers.CustomerOrderTrackSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': _("Invalid order tracking ID")}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: serializers.CustomerOrderLiveTrackSerializer})
    @action(detail=False, methods=['get'], url_path='(?P<tracking_id>[^/.]+)/tracklive')
    def track_live(self, request, tracking_id):
        try:
            order = Order.objects.get(invoice_no=tracking_id, customer=self.request.user)
            delivery = OrderDelivery.objects.get(order=order)
            serializer = serializers.CustomerOrderLiveTrackSerializer(delivery)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Live tracking is not available yet.'},
                            status=status.HTTP_400_BAD_REQUEST)


class CustomerAddressAPI(viewsets.ModelViewSet):
    permission_classes = [IsCustomer, ]
    queryset = Address.objects.all()
    serializer_class = serializers.CustomerAddressSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Order.objects.filter(shipping_address=instance).exists():
            return Response(
                {'detail': [_("Address associated with an order.")]}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class CustomerReasonAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Reason.objects.filter(is_active=True)
    serializer_class = serializers.CustomerReasonSerializer


class CustomerCouponAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Coupon.objects.all()
    serializer_class = serializers.CustomerCouponSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = Coupon.objects.filter(customers__in=[user])
        return queryset
