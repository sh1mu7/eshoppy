from django.db import models
from django.conf import settings
from coreapp.base import BaseModel
from subscription import constants


class CustomerInformation(BaseModel):
    user = models.OneToOneField('coreapp.User', on_delete=models.DO_NOTHING)
    reward_points = models.DecimalField(max_length=10, decimal_places=2, default=0.0)
    membership_type = models.SmallIntegerField(choices=constants.MembershipType.choices,
                                               default=constants.MembershipType.GENERAL)
    device_id = models.CharField(max_length=255)


class Package(BaseModel):
    package_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    is_active = models.BooleanField(default=True)


class SubscriptionHistory(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('subscription.Package', on_delete=models.CASCADE)
    start_date = models.DateField()
    expiry_date = models.DateField()
    is_expired = models.BooleanField(default=False)
