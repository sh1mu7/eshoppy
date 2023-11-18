from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypeChoices(models.IntegerChoices):
    INFO = 1, 'Information'
    WARNING = 2, 'Warning'
    ERROR = 3, 'Error'

