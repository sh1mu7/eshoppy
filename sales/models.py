from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property

from coreapp.base import BaseModel
from delivery.models import OrderDelivery
from sales import constants
from sales.utils import coupon_utils
from sales.utils.order_utils import generate_order_reference
from utility.constants import PaymentMethod


class Reason(BaseModel):
    reason_type = models.SmallIntegerField(choices=constants.ReasonType.choices)
    reason_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=15, editable=False, unique=True, null=False, blank=False)
    coupon_title = models.CharField(max_length=100)
    coupon_type = models.SmallIntegerField(choices=constants.CouponType.choices)
    discount_type = models.SmallIntegerField(choices=constants.DiscountType.choices)
    start_date = models.DateTimeField()
    expire_date = models.DateTimeField()
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    maximum_discount = models.IntegerField(null=True)
    max_usage = models.IntegerField()
    usage_count = models.IntegerField(default=0)
    customers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='coupons')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code

    def save(self, *args, **kwargs):
        self.coupon_code = coupon_utils.generate_coupon_code()
        super(Coupon, self).save(**kwargs)


class Order(BaseModel):
    invoice_no = models.CharField(default=generate_order_reference, max_length=50, editable=False, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='order_staff',
                                    null=True, blank=True)
    delivery_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       related_name='order_delivery_staff', null=True, blank=True)
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
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.SmallIntegerField(choices=PaymentMethod.choices)
    payment_status = models.SmallIntegerField(choices=constants.PaymentStatus.choices,
                                              default=constants.PaymentStatus.PENDING)
    estd_delivery_time = models.DateField(null=True, blank=True)
    order_status = models.SmallIntegerField(choices=constants.OrderStatus.choices,
                                            default=constants.OrderStatus.PENDING)
    order_stage = models.SmallIntegerField(choices=constants.OrderStage.choices,
                                           default=constants.OrderStage.ORDER_PLACED)
    cancel_status = models.SmallIntegerField(choices=constants.OrderCancelStatus.choices, default=None, null=True)
    has_cancel_request = models.BooleanField(default=False)
    cancel_reason = models.ForeignKey('sales.Reason', on_delete=models.CASCADE, null=True, blank=True)
    cancel_reason_note = models.TextField(null=True, blank=True)

    @cached_property
    def get_order_item(self):
        return self.orderitem_set.all()

    @cached_property
    def get_item_count(self):
        return self.orderitem_set.count()

    @cached_property
    def get_customer_name(self):
        return self.customer.get_full_name


    @cached_property
    def get_customer_email(self):
        return self.customer.email

    @cached_property
    def get_customer_mobile(self):
        return self.customer.mobile

    @cached_property
    def get_order_staff(self):
        return self.delivery_staff.get_full_name

    @cached_property
    def get_order_event_status(self):
        return self.orderevent_set.all()

    @cached_property
    def check_order_status(self):
        return self.get_order_event_status

    @cached_property
    def get_delivery_status(self):
        try:
            order_delivery=OrderDelivery.objects.get(order_id=self.id)
            return order_delivery.status
        except OrderDelivery.DoesNotExist:
            return None


class OrderItem(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    product_variant = models.ForeignKey('inventory.ProductVariant', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @cached_property
    def get_product_name(self):
        return self.product.name

    @cached_property
    def get_product_image_url(self):
        return self.product.get_thumbnail_url

    @cached_property
    def get_product_price(self):
        if self.product_variant:
            price = self.product_variant.additional_price + self.product.price
            return price
        else:
            price = self.product.price
            return price

    @cached_property
    def get_subtotal(self):
        if self.product_variant:
            subtotal = (Decimal(self.get_product_price) * Decimal(self.quantity))
            return subtotal
        else:
            subtotal = Decimal(self.price) * Decimal(self.quantity)
            return subtotal

    @cached_property
    def get_vat_amount(self):
        vat = self.get_subtotal * (self.product.vat / 100)
        return vat

    @cached_property
    def get_total(self):
        total = self.subtotal + self.get_vat_amount
        return total

    @cached_property
    def get_avg_rating(self):
        return self.product.average_rating

    @cached_property
    def get_total_review(self):
        return self.product.total_review

    @cached_property
    def get_product_category(self):
        category = self.product.category.id
        return category

    @cached_property
    def get_is_featured(self):
        if self.product.is_featured:
            return True
        return False

    @cached_property
    def get_has_variant(self):
        if self.product.has_variant:
            return True
        return False

    def save(self, *args, **kwargs):
        self.price = self.get_product_price
        self.vat_amount = self.get_vat_amount
        self.subtotal = self.get_subtotal
        self.total = self.get_total
        order = self.order
        total_reward_points = OrderItem.objects.filter(order=order).aggregate(Sum('product__reward_points'))[
            'product__reward_points__sum']
        order.reward_points = total_reward_points if total_reward_points else 0
        order.save()
        super(OrderItem, self).save(*args, **kwargs)


class OrderEvent(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, related_name='events')
    event_status = models.SmallIntegerField(choices=constants.OrderEventStatus.choices,
                                            default=constants.OrderEventStatus.ORDER_PLACED)
    note = models.TextField()

    def __str__(self):
        return f'Order: {self.order.invoice_no} Order Status:{self.event_status.__str__()}'


class OrderReturn(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, related_name='order_return')
    customer = models.ForeignKey('coreapp.User', on_delete=models.CASCADE)
    customer_mobile = models.CharField(max_length=15)
    reason = models.ForeignKey('sales.Reason', on_delete=models.CASCADE)
    image = models.ManyToManyField('coreapp.Document')
    refund_method = models.SmallIntegerField(choices=PaymentMethod.choices)
    reason_detail = models.TextField()
    return_status = models.SmallIntegerField(choices=constants.OrderReturnStatus.choices,
                                             default=constants.OrderReturnStatus.PENDING)
    event_status = models.SmallIntegerField(choices=constants.OrderEventStatus.choices,
                                            default=constants.OrderEventStatus.REQUEST_SENT)

    def __str__(self):
        return f'{self.order} and returned by {self.return_status}, customer mobile {self.customer_mobile}'
