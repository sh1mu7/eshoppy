from django.db import models
from django.conf import settings
from coreapp.base import BaseModel
from support import constants


class SupportTicket(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=constants.TicketStatusChoices.choices,
                              default=constants.TicketStatusChoices.OPEN)
    priority = models.CharField(max_length=20, choices=constants.PriorityChoices.choices,
                                default=constants.PriorityChoices.LOW)
    attachment = models.ManyToManyField('coreapp.Document')

    def __str__(self):
        return f'{self.user.get_full_name} -- {self.subject} -- {self.status}'


class TicketReply(BaseModel):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    note = models.TextField()
    attachment = models.ManyToManyField('coreapp.Document')
