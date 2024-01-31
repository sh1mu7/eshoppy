from datetime import datetime

from dateutil.relativedelta import relativedelta

from cart.models import Cart
from coreapp.constants import MembershipAndPackageType
from coreapp.models import Address
from delivery.utils.distance_utils import haversine, nearest_delivery_charge
from inventory.models import ProductVariant
from sales.utils import coupon_utils
from utility.models import GlobalSettings


class ProductOutOfStockError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class CouponNotFoundError(Exception):
    pass


def process_cart_and_coupon(customer, subtotal, vat_amount, order, cart_items_id, coupon_code, quantity_list):
    from sales.models import OrderItem, Coupon
    discount = 0
    for index, cart_item_id in enumerate(cart_items_id):
        try:
            cart_item = Cart.objects.get(user=customer, id=cart_item_id)
            product = cart_item.product
            quantity = quantity_list[index]

            order_item = OrderItem.objects.create(
                order=order, customer=customer, product=product, quantity=quantity,
                vat_amount=product.get_vat_amount, product_variant=cart_item.product_variant)
            order_item.save()
            subtotal += order_item.subtotal
            vat_amount += order_item.get_vat_amount
            if cart_item.product_variant:
                product_variant = ProductVariant.objects.get(id=cart_item.product_variant.id)
                product_variant.quantity -= cart_item.quantity
                product_variant.save()
            else:
                product.quantity -= cart_item.quantity
                product.save()
        except Cart.DoesNotExist:
            raise CartItemNotFoundError('Cart item not found.')

    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            order.coupon_id = coupon.id
            discount += coupon_utils.discount_after_coupon(subtotal, coupon, order.customer)
        except Coupon.DoesNotExist:
            raise CouponNotFoundError('Coupon not found.')
    return subtotal, vat_amount, discount


def adjust_estd_delivery_time(order):
    now = datetime.now()
    if order.customer.membership_type == MembershipAndPackageType.BASIC:
        return (now + relativedelta(days=5)).date()
    elif order.customer.membership_type == MembershipAndPackageType.PREMIUM:
        return (now + relativedelta(days=4)).date()
    elif order.customer.membership_type == MembershipAndPackageType.VIP:
        return (now + relativedelta(days=2)).date()
    elif order.customer.membership_type is None:
        return (now + relativedelta(days=7)).date()


def shipping_charge_calculate(user):
    address = Address.objects.get(user_id=user.id, is_default=True)
    global_setting = GlobalSettings.objects.first()
    store_latitude = global_setting.latitude
    store_longitude = global_setting.longitude
    distance = haversine(address.latitude, address.longitude, store_latitude, store_longitude)
    shipping_charge = nearest_delivery_charge(round(distance, 2))
    return shipping_charge
