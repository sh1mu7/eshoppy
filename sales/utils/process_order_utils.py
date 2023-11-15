from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from cart.models import Cart
from coreapp.utils.auth_utils import get_client_info
from inventory.models import ProductVariant, Product
from sales import constants
from sales.models import OrderItem, Coupon, OrderEvent
from sales.utils import coupon_utils
from utility.models import Payment
from utility import constants as payment_constants


class ProductOutOfStockError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class CouponNotFoundError(Exception):
    pass


def process_cart_and_coupon(customer, subtotal, vat_amount, order, cart_items_id, coupon_code):
    discount = 0
    for cart_item_id in cart_items_id:
        try:
            cart_item = Cart.objects.get(user=customer, id=cart_item_id)
            product = cart_item.product
            if not product.has_stock:
                raise ProductOutOfStockError(f'{product.product_name} is out of stock.')
            order_item = OrderItem.objects.create(
                order=order, customer=customer, product=product, quantity=cart_item.quantity,
                vat_amount=product.get_vat_amount, product_variant=cart_item.product_variant)
            order_item.save()
            subtotal += order_item.subtotal
            vat_amount += order_item.get_vat_amount

            if cart_item.product_variant:
                product_variant = ProductVariant.objects.get(id=cart_item.product_variant.id)
                if not product_variant.has_stock:
                    raise ProductOutOfStockError(
                        f'The variant of the product "{product_variant.product.name}" with code {product_variant.code}'
                        f' is currently unavailable.')
                product_variant.quantity = product_variant.quantity - cart_item.quantity
                product_variant.save()
            else:
                product.quantity = product.quantity - cart_item.quantity
                product.save()
        except Cart.DoesNotExist:
            raise CartItemNotFoundError('Cart item not found.')

    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            order.coupon_id = coupon.id
            discount += coupon_utils.discount_after_coupon(subtotal, coupon)
        except Coupon.DoesNotExist:
            raise CouponNotFoundError('Coupon not found.')
    return subtotal, vat_amount, discount
