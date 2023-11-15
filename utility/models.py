import uuid
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
import coreapp.roles
from coreapp.base import BaseModel
from utility import constants
from .utils import slug_utils


class GlobalSettings(BaseModel):
    site_name = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100)
    logo = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    latitude = models.DecimalField(decimal_places=16, max_digits=20, default=0.00)
    longitude = models.DecimalField(decimal_places=16, max_digits=20, default=0.00)
    short_desc = models.TextField(max_length=500)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    shipping_fee = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    vat_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    min_withdraw_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    max_withdraw_amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    payment_gateway_key = models.CharField(max_length=100)
    payment_gateway_secret = models.CharField(max_length=100)
    payment_gateway_uid = models.CharField(max_length=100)
    payment_gateway_server = models.CharField(max_length=100)
    sms_server = models.CharField(max_length=100)
    sms_username = models.CharField(max_length=100)
    sms_phone_number = models.CharField(max_length=100)
    sms_api_key = models.CharField(max_length=100)
    user_fcm_key = models.CharField(max_length=100)
    rider_fcm_server_key = models.CharField(max_length=100)
    sender_email = models.CharField(max_length=100)
    email_host = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    port = models.CharField(max_length=10)

    @cached_property
    def get_logo_url(self):
        return self.logo.get_url

    @cached_property
    def get_shipping_fee(self):
        return self.shipping_fee

    def __str__(self):
        return self.site_name


class Currency(BaseModel):
    currency_name = models.CharField(max_length=15)
    currency_sign = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)
    currency_rate = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

    @cached_property
    def get_currency_sign_url(self):
        return self.currency_sign.get_url

    def __str__(self):
        return self.currency_name


class Page(BaseModel):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    slug = models.CharField(max_length=100, unique=True, db_index=True, editable=False)
    thumbnail = models.ForeignKey("coreapp.Document", on_delete=models.CASCADE, related_name="page_thumbnail")
    attachment = models.ForeignKey(
        "coreapp.Document", on_delete=models.CASCADE,
        related_name="page_attachment", null=True, blank=True
    )
    video_url = models.CharField(max_length=100, null=True, blank=True)
    page_type = models.IntegerField(choices=constants.PageType.choices)
    is_active = models.BooleanField(default=0)

    def __str__(self):
        return self.title

    @cached_property
    def get_thumbnail_url(self):
        return self.thumbnail.get_url

    @cached_property
    def get_attachment_url(self):
        return self.attachment.get_url

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_utils.generate_unique_slug(self.title, self)
        super(Page, self).save(**kwargs)


class BankInformation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)


class WalletRecharge(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_code = models.CharField(max_length=100)
    transaction_no = models.CharField(max_length=100)
    note = models.TextField()
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.amount} - {self.bill_code} - {self.transaction_no}"


class Payment(BaseModel):
    uid = models.UUIDField(default=uuid.uuid4, db_index=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ip_address = models.CharField(max_length=100)
    transaction_type = models.SmallIntegerField(choices=constants.TransactionType.choices)
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey('subscription.SubscriptionHistory', on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(choices=constants.PaymentStatus.choices, default=constants.PaymentStatus.PENDING)
    payment_method = models.SmallIntegerField(choices=constants.PaymentMethod.choices)
    bill_uid = models.CharField(max_length=100, null=True, blank=True)
    bill_url = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.bill_uid


class Payout(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank = models.ForeignKey('utility.BankInformation', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)


class Refund(models.Model):
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refunds_requested')
    cancel_reason = models.ForeignKey('sales.Reason', on_delete=models.CASCADE)
    canceled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='refunds_processed')
    user_type = models.IntegerField(choices=coreapp.roles.UserRoles.choices)
    comment = models.TextField()
    refundable_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Banner(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)
    expiry_date = models.DateField()
    position = models.IntegerField()
    is_active = models.BooleanField(default=True)

    @cached_property
    def get_image_url(self):
        return self.image.get_url

    def __str__(self):
        return self.name


class FAQ(BaseModel):
    faq_type = models.IntegerField(choices=constants.FaqType.choices, default=constants.FaqType.Customer)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    position = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class SearchResult(BaseModel):
    search_text = models.CharField(max_length=200)
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.search_text
