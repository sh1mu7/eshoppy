from django.db import models
from django.utils.translation import gettext_lazy as _


class CommissionStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    SETTLED = 1, _('Settled')
    ON_PROCESSING = 2, _('On Processing')



