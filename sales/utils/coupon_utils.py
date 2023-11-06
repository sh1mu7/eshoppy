import decimal
import string
import random
from sales import constants


def discount_after_coupon(subtotal, coupon):
    if coupon.discount_type == constants.DiscountType.FLAT:
        return coupon.price
    elif coupon.discount_type == constants.DiscountType.PERCENTAGE:
        discount_amount = decimal.Decimal(subtotal * coupon.price / 100)
        if discount_amount > coupon.maximum_discount_amount:
            return coupon.maximum_discount_amount
        else:
            return discount_amount
    else:
        return 15


def generate_coupon_code():
    characters = list(string.ascii_uppercase + string.digits)
    random.shuffle(characters)
    coupon_code = ''.join(characters[:8])
    formatted_coupon_code = f"{coupon_code[:4]}-{coupon_code[4:]}"
    return formatted_coupon_code


# def generate_coupon_code():
#     random_number = random.randint(100000, 999999)
#     return f"CPN-{random_number}"
