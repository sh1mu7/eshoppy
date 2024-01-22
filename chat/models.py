from django.db import models
from django.conf import settings

from coreapp.base import BaseModel


class Message(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    attachment = models.ManyToManyField('coreapp.Document')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.get_full_name} sends message to {self.receiver.get_full_name}'

    def get_receiver_name(self):
        return self.receiver.get_full_name

    def get_sender_name(self):
        return self.sender.get_full_name
