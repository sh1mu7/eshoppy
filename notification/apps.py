from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials

from notification import firebase


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
