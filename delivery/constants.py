from django.db import models
from django.utils.translation import gettext_lazy as _


class CommissionStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    SETTLED = 1, _('Settled')
    ON_PROCESSING = 2, _('On Processing')


class RiderOrderDeliveryStatus(models.IntegerChoices):
    ON_GOING = 0, _('On Going')
    PICKED = 1, _('Picked')
    ACTIVE = 2, _('Active')
    COMPLETED = 3, _('Completed')
