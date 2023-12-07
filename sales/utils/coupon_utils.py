import decimal
import string
import random
from sales import constants
from utility.utils.settings_utils import settings_object


def discount_after_coupon(subtotal, coupon):
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
        return settings_object.shipping_fee


def generate_coupon_code():
    characters = list(string.ascii_uppercase + string.digits)
    random.shuffle(characters)
    coupon_code = ''.join(characters[:8])
    formatted_coupon_code = f"{coupon_code[:4]}-{coupon_code[4:]}"
    return formatted_coupon_code
