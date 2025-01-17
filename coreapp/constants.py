from django.db import models
from django.utils.translation import gettext_lazy as _


# Gender  Options
class GenderChoices(models.IntegerChoices):
    MALE = 0, _("Male")
    FEMALE = 1, _("Female")
    OTHER = 2, _("Other")


# Document  Options
class DocumentChoices(models.IntegerChoices):
    IMAGE = 0, _("Image")
    VIDEO = 1, _("Video")
    FILE = 2, _("File")
    OTHER = 3, _("Other")


class MembershipAndPackageType(models.IntegerChoices):
    BASIC = 0, _('Basic')
    PREMIUM = 1, _('Premium')
    VIP = 2, _('VIP')


class AddressType(models.IntegerChoices):
    HOME = 0, _('Home')
    OFFICE = 1, _('Office')
    OTHER=2, _('Other')
