from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'notifications', views.UserNotificationAPI)
urlpatterns = []
urlpatterns += router.urls
