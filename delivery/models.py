from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from coreapp.base import BaseModel
from coreapp.models import Address
from delivery import constants
from sales import constants as order_constants
from utility.models import GlobalSettings


class RiderDocuments(BaseModel):
    title = models.CharField(max_length=100)
    documents = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)

    def get_documents_url(self):
        return self.documents.get_url


class DeliveryRider(BaseModel):
    delivery_man = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vehicle_type = models.CharField(max_length=50)
    rider_documents = models.ManyToManyField(RiderDocuments)


class DeliveryRequest(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_staff')
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='request_rider')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.order.invoice_no


class OrderDelivery(BaseModel):
    delivery_request = models.ForeignKey('delivery.DeliveryRequest', on_delete=models.CASCADE)
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ordered_customer')
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_rider')
    estd_delivery_time = models.DateField()
    status = models.SmallIntegerField(choices=order_constants.DeliveryStatus.choices)
    rider_delivery_status = models.SmallIntegerField(choices=constants.RiderOrderDeliveryStatus.choices,
                                                     default=constants.RiderOrderDeliveryStatus.ACTIVE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def get_order_invoice(self):
        return self.order.invoice_no

    def get_payment_status(self):
        return self.order.payment_status


class DeliveryCharge(BaseModel):
    km_distance = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


class RiderCommission(BaseModel):
    rider = models.ForeignKey(DeliveryRider, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    commission_status = models.SmallIntegerField(choices=constants.CommissionStatus.choices,
                                                 default=constants.CommissionStatus.PENDING)

# TODO: What's the commission structure does it based on a fixed rate per delivery or percentage of the total delivery?
