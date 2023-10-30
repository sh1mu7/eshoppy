import decimal
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
