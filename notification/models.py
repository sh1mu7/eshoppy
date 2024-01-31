from django.db import models
from django.utils.functional import cached_property
from coreapp.base import BaseModel
from django.conf import settings
from notification.constants import TypeChoices


class Notification(BaseModel):
    notification_type = models.SmallIntegerField(choices=TypeChoices.choices)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_sender',
                               null=True)
    recipient = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notification_recipient')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    @cached_property
    def get_sender_name(self):
        return self.sender.get_full_name

    @cached_property
    def get_sender_image(self):
        return self.sender.get_image_url

    def __str__(self):
        return self.message
