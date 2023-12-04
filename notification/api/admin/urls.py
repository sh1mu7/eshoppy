from django.urls import path, include
from rest_framework import routers
from .views import AdminSystemAlertAPI, AdminPersonalNotificationAPI

router = routers.DefaultRouter()
router.register('system-alert', AdminSystemAlertAPI)
router.register('personal-notification', AdminPersonalNotificationAPI)
urlpatterns = [

]
urlpatterns += router.urls
