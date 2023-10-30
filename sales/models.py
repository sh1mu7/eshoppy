from django.conf import settings
from django.db import models
from coreapp.base import BaseModel
from sales import constants
from sales.utils.order_utils import generate_order_reference
from utility.constants import PaymentMethod


class Reason(BaseModel):
    reason_type = models.SmallIntegerField()
    reason_name = models.CharField(max_length=255)


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_type = models.SmallIntegerField(choices=constants.DiscountType.choices)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_discount = models.IntegerField()
    total_used = models.IntegerField(default=0)
    belonging_category = models.ManyToManyField('inventory.Category', related_name='coupons')
    products = models.ManyToManyField('inventory.Product', related_name='coupons')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='coupons')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code


class Order(BaseModel):
    invoice_no = models.CharField(default=generate_order_reference, max_length=50, editable=False, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_stuff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_note = models.TextField(blank=True)
    customer_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    customer_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    reward_points = models.IntegerField(default=0)
    shipping_address = models.ForeignKey('coreapp.Address', on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey('sales.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=PaymentMethod.choices)
    payment_status = models.SmallIntegerField(choices=constants.PaymentStatus.choices,
                                              default=constants.PaymentStatus.PENDING)
    estd_delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_status = models.SmallIntegerField(choices=constants.DeliveryStatus.choices,
                                               default=constants.OrderStatus.PENDING)
    order_status = models.SmallIntegerField(choices=constants.OrderStatus.choices,
                                            default=constants.OrderStatus.PROCESSING)
    cancel_reason = models.ForeignKey('sales.Reason', on_delete=models.CASCADE, null=True, blank=True)
    cancel_reason_note = models.TextField(null=True, blank=True)


class OrderItem(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
    product = models.ForeignKey('inventory.ProductVariant', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class OrderEvent(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    event_status = models.SmallIntegerField(choices=constants.OrderEventStatus.choices,
                                            default=constants.OrderEventStatus.ORDER_PLACED)
    note = models.TextField()
