from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from cart.models import Cart
from coreapp.models import Address
from coreapp.permissions import IsCustomer
from coreapp.utils.auth_utils import get_client_info
from inventory.models import Product, ProductVariant
from sales.models import Reason, Coupon, Order, OrderItem, OrderEvent
from utility.models import Payment
from utility.utils.payment_utils import generate_bill_url
from . import serializers
from ... import constants
from utility import constants as payment_constants
from ...utils import coupon_utils


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
                for item in cart_items:
                    if not item.product.has_stock:
                        return Response({'detail': f'{item.product.product_name} is out of stock.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    order_item = OrderItem.objects.create(
                        order=order, customer=customer, product=item.product, quantity=item.quantity,
                        vat_amount=item.product.get_vat_amount, product_variant=item.product_variant)
                    order_item.save()
                    subtotal = subtotal + order_item.subtotal
                    vat_amount += order_item.get_vat_amount
                    if item.product_variant:
                        product_variant = ProductVariant.objects.get(id=item.product_variant.id)
                        if not product_variant.has_stock:
                            return Response(
                                {'detail': [
                                    _(f'The variant of the product "{product_variant.product.name}" with code {product_variant.code}'
                                      f' is currently unavailable.')]}, status=status.HTTP_400_BAD_REQUEST)
                        product_variant.quantity = product_variant.quantity - item.quantity
                        product_variant.save()
                    else:
                        product = Product.objects.get(id=item.product.id)
                        product.quantity = product.quantity - item.quantity
                if coupon_code:
                    coupon = Coupon.objects.get(coupon_code=coupon_code)
                    order.coupon_id = coupon.id
                    discount += coupon_utils.discount_after_coupon(subtotal, coupon)
                order.subtotal = subtotal
                order.vat = vat_amount
                total += subtotal + vat_amount + shipping_charge - discount
                order.total = total
                order.save()
                order.refresh_from_db()
                # TODO: Need to remove the comment
                # cart_items.delete()
                OrderEvent.objects.create(order=order, event_status=constants.OrderEventStatus.ORDER_PLACED,
                                          note='Order has been placed successfully').save()
                ip, user_agent = get_client_info(request)

                payment = Payment.objects.create(
                    amount=total, ip_address=ip, order=order, status=payment_constants.PaymentStatus.PENDING,
                    transaction_type=payment_constants.TransactionType.ORDER, payment_method=payment_method,
                    user=self.request.user).save()
                # if not payment_method == payment_constants.PaymentMethod.CASH:
                #     bill_url = generate_bill_url(payment)
                #     if not bill_url:
                #         return Response({'detail': 'Bill Url.'}, status=status.HTTP_400_BAD_REQUEST)
                # else:
                #     bill_url = None
                # TODO: Need to setup the payment configuration
                data = {
                    'detail': 'Order has been placed successfully.',
                    # 'bill_url': bill_url,
                    # 'tracking_id': order.invoice_no,
                    # 'order_id': order.id
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'detail': [_(f"{str(e)} can not create order. Try again.")]})


class CustomerAddressAPI(viewsets.ModelViewSet):
    permission_classes = [IsCustomer, ]
    queryset = Address.objects.all()
    serializer_class = serializers.CustomerAddressSerializer


class CustomerReasonAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Reason.objects.all()
    serializer_class = serializers.CustomerReasonSerializer


class CustomerCouponAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Coupon.objects.all()
    serializer_class = serializers.CustomerCouponSerializer

    def get_queryset(self):
        user = self.request.user.id
        queryset = Coupon.objects.filter(customers=user)
        return queryset
