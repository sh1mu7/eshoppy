from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class TicketStatusChoices(IntegerChoices):
    OPEN = 1, _('Open')
    CLOSED = 2, _('Closed')
    IN_PROGRESS = 3, _('In Progress')


class PriorityChoices(IntegerChoices):
    LOW = 1, _('Low')
    MEDIUM = 2, _('Medium')
    HIGH = 3, _('High')
