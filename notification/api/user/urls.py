from django.urls import path, include
from rest_framework import routers
from .views import UserSystemAlertAPI, UserPersonalNotificationAPI

router = routers.DefaultRouter()
router.register('system-alert', UserSystemAlertAPI)
router.register('personal-notification', UserPersonalNotificationAPI)
urlpatterns = [

]
urlpatterns += router.urls
