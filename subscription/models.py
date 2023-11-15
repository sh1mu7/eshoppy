from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from coreapp.base import BaseModel


class Package(BaseModel):
    package_name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(default=1)
    details = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.package_name

    def save(self, *args, **kwargs):
        self.generate_slug('package_name')
        super(Package, self).save(*args, **kwargs)


class SubscriptionHistory(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('subscription.Package', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_expired = models.BooleanField(default=False, editable=False)

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

    @cached_property
    def get_package_details(self):
        return self.package.details

    @cached_property
    def get_package_price(self):
        return self.package.price

    @cached_property
    def get_is_expired(self):
        now = datetime.now()
        expiry_datetime = datetime.combine(self.expiry_date, datetime.min.time())

        if expiry_datetime < now:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        super(SubscriptionHistory, self).save(*args, **kwargs)
