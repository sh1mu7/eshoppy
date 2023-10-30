from django.db import models
from django.conf import settings

from coreapp.base import BaseModel
from delivery import constants


class RiderDocuments(BaseModel):
    title = models.CharField(max_length=100)
    documents = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)


class DeliveryRider(BaseModel):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2)
    device_id = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    image = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)
    rider_documents = models.ManyToManyField(RiderDocuments)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class DeliveryRequest(BaseModel):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=True)


class OrderDelivery(BaseModel):
    delivery_request = models.ForeignKey('delivery.DeliveryRequest', on_delete=models.CASCADE)
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    estd_delivery_time = models.DateTimeField()
    address = models.TextField()


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
