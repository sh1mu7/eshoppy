from django.db import models
from django.conf import settings
from coreapp.base import BaseModel
from notification import constants


class SystemAlert(BaseModel):
    title = models.CharField(max_length=100)
    message = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PersonalNotification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField()
    notification_type = models.SmallIntegerField(choices=constants.NotificationTypeChoices.choices)
