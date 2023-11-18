from django.urls import path, include
from rest_framework import routers
from .views import AdminSystemAlertAPI

router = routers.DefaultRouter()
router.register('system', AdminSystemAlertAPI)
urlpatterns = [
    path('', include(router.urls))
]
