from django.db import models
from django.utils.translation import gettext_lazy as _


class MembershipType(models.IntegerChoices):
    PREMIUM = 0, _('Premium')
    GENERAL = 1, _('General')
