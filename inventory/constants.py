from django.db import models
from django.utils.translation import gettext_lazy as _


class StockStatusChoices(models.IntegerChoices):
    IN_STOCK = 0, _('In Stock')
    OUT_OF_STOCK = 1, _('Out of Stock')
    COMING_SOON = 2, _('Coming Soon')
