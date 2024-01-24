import decimal
import random
import string

from coreapp.utils.twilio_utils import get_system_settings
from sales import constants
from sales.utils.process_order_utils import shipping_charge_calculate

settings_object = get_system_settings()


def discount_after_coupon(subtotal, coupon, user):
    print(subtotal, coupon)
    if coupon.coupon_type == constants.CouponType.FIRST_ORDER:
        if coupon.discount_type == constants.DiscountType.AMOUNT:
            if subtotal > coupon.minimum_purchase:
                return coupon.discount_amount
            else:
                discount_amount = decimal.Decimal(subtotal * coupon.discount_amount / 100)
                if discount_amount > coupon.maximum_discount and subtotal > coupon.minimum_purchase:
                    return coupon.maximum_discount
                else:
                    return discount_amount
    elif coupon.coupon_type == constants.CouponType.DISCOUNT_ON_PURCHASE:
        if coupon.discount_type == constants.DiscountType.AMOUNT:
            if subtotal > coupon.minimum_purchase:
                return coupon.discount_amount
            else:
                discount_amount = decimal.Decimal(subtotal * coupon.discount_amount / 100)
                if discount_amount > coupon.maximum_discount and subtotal > coupon.minimum_purchase:
                    return coupon.maximum_discount
                else:
                    return discount_amount
    else:
        shipping_charge = shipping_charge_calculate(user)
        print(shipping_charge)
        return shipping_charge


def generate_coupon_code():
    characters = list(string.ascii_uppercase + string.digits)
    random.shuffle(characters)
    coupon_code = ''.join(characters[:8])
    formatted_coupon_code = f"{coupon_code[:4]}-{coupon_code[4:]}"
    return formatted_coupon_code
