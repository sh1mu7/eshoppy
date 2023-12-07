from django.db import models
from django.utils.translation import gettext_lazy as _


class ReasonType(models.IntegerChoices):
    CHANGE_OF_MIND = 0, _('Change Of Mind')
    ITEM_OUT_OF_STOCK = 1, _('Item Out of Stock')
    CUSTOMER_REQUEST = 2, _('Customer Request')
    BY_ADMIN = 3, _('By Admin')


class OrderStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    PROCESSING = 1, _('Processing')
    SHIPPED = 2, _('Shipped')
    OUT_OF_DELIVERY = 3, _('Out of delivery')
    DELIVERED = 4, _('Delivered')
    CANCELED = 5, _('Canceled')
    REFUNDED = 6, _('Refunded')


class OrderStage(models.IntegerChoices):
    ORDER_PLACED = 0, _('Order Placed')
    REQUEST_SENT = 1, _('Request Sent')
    DELIVERYMAN_ASSIGNED = 2, _('Deliveryman Assigned')
    DELIVERED = 3, _('Delivered')


class OrderEventStatus(models.IntegerChoices):
    ORDER_PLACED = 0, _('Order Placed')
    REQUEST_SENT = 1, _('Request Sent')
    DELIVERYMAN_ASSIGNED = 2, _('Deliveryman Assigned')
    DELIVERED = 3, _('Delivered')


class OrderCancelStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    ACCEPT = 1, _('Accept')
    REJECT = 2, _('Reject')


class DeliveryStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    ON_GOING = 1, _('On Going')
    PICKED = 2, _('Picked')
    ACTIVE = 3, _('Active')
    COMPLETED = 4, _('Completed')
    CANCELED = 5, _('Canceled')
    RETURNED = 6, _('Returned')


class PaymentStatus(models.IntegerChoices):
    SUCCEED = 0, _('Succeed')
    FAILED = 1, _('Failed')
    PENDING = 2, _('Pending')


class CouponType(models.IntegerChoices):
    FREE_DELIVERY = 0, _('Free Delivery')
    FIRST_ORDER = 1, _('First Order')
    DISCOUNT_ON_PURCHASE = 2, _('Discount On Purchase')


class DiscountType(models.IntegerChoices):
    AMOUNT = 0, _('Amount')
    PERCENTAGE = 1, _('Percentage')
