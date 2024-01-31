from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from coreapp import constants, roles
from coreapp.manager import MyUserManager
from .base import BaseModel, compress_image


class Country(BaseModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    phone_code = models.CharField(_("Phone code"), max_length=50)
    flag = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Address(BaseModel):
    address_type = models.SmallIntegerField(choices=constants.AddressType.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_address')
    country = models.ForeignKey('coreapp.Country', on_delete=models.CASCADE)
    flat = models.CharField(max_length=100)
    road = models.CharField(max_length=255)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=20, decimal_places=14, default=0.00)
    longitude = models.DecimalField(max_digits=20, decimal_places=14, default=0.00)
    is_default = models.BooleanField(default=False)

    def make_default(self):
        Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True

    def get_country_name(self):
        return self.country.name

    def __str__(self):
        return f"User: {self.user.get_full_name}\nAddress:{self.flat}, {self.road}, {self.address}, {self.country}, {self.zip_code}"

    def save(self, *args, **kwargs):
        if self.is_default:
            self.make_default()
        super(Address, self).save(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(unique=True, max_length=20)
    dob = models.DateField()
    image = models.ForeignKey('coreapp.Document', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.SmallIntegerField(choices=constants.GenderChoices.choices, default=constants.GenderChoices.MALE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    role = models.IntegerField(choices=roles.UserRoles.choices, default=roles.UserRoles.CUSTOMER)
    reward_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    membership_type = models.SmallIntegerField(choices=constants.MembershipAndPackageType.choices, null=True)
    fcm_token = models.CharField(max_length=255, null=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @cached_property
    def get_image_url(self):
        return self.image.get_url if self.image_id else None

    @cached_property
    def get_country_name(self):
        return self.country.name

    def get_membership_type(self):
        if self.membership_type:
            return self.membership_type
        else:
            return None

    def get_default_address(self):
        try:
            return self.user_address.get(is_default=True)
        except Address.DoesNotExist:
            return None


class UserConfirmation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.confirmation_code} : {self.is_used}"


class LoginHistory(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=500)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.user_agent} - {self.is_success}"


class Document(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    doc_type = models.SmallIntegerField(choices=constants.DocumentChoices.choices)

    def __str__(self):
        return f"{self.owner} - {self.document.name}"

    @cached_property
    def get_url(self):
        return f"{settings.MEDIA_HOST}{self.document.url}"

    @cached_property
    def get_filename(self):
        return f"{self.document.url}"

    # def save(self, *args, **kwargs):
    #     image = compress_image(self.document)
    #     if self.document:
    #         self.document = image
    #     super(Document, self).save(*args, **kwargs)
