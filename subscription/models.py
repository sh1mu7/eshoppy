from django.db import models
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from coreapp.base import BaseModel
from subscription import constants


class CustomerInformation(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    reward_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    membership_type = models.SmallIntegerField(choices=constants.MembershipType.choices,
                                               default=constants.MembershipType.GENERAL)
    device_id = models.CharField(max_length=255)

    @cached_property
    def get_customer_name(self):
        return self.user.get_full_name


class Package(BaseModel):
    package_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.package_name


class SubscriptionHistory(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('subscription.Package', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} - {self.package} - {self.expiry_date}"

    @cached_property
    def get_customer_name(self):
        return self.customer.get_full_name

    @cached_property
    def get_package_name(self):
        return self.package.package_name

    @cached_property
    def get_package_duration(self):
        return self.package.duration

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.expiry_date = now + relativedelta(months=self.package.duration)
        if self.expiry_date < now.date():
            self.is_expired = True
        else:
            self.is_expired = False
        super(SubscriptionHistory, self).save(*args, **kwargs)
