from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.IntegerChoices):
    ADMIN = 0, _('ADMIN')
    ADMIN_STAFF = 1, _("Admin Staff")
    CUSTOMER = 2, _("Customer")
    DELIVERY_STAFF = 3, _("Delivery Staff")
