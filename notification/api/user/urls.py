from django.urls import path, include
from rest_framework import routers
from .views import UserSystemAlertAPI

router = routers.DefaultRouter()
router.register('system', UserSystemAlertAPI)
urlpatterns = [
    path('', include(router.urls))
]
