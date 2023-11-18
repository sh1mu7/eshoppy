from django.urls import path, include
from rest_framework import routers
from .views import RiderProfileAPI, RiderDeliveryRequestAPI

router = routers.DefaultRouter()
router.register('profile', RiderProfileAPI)
router.register('delivery_request', RiderDeliveryRequestAPI)
urlpatterns = [
    path('', include(router.urls))
]
