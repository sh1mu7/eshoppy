from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypeChoices(models.IntegerChoices):
    USER = 0, _('User')
    SYSTEM = 1, _('System')

