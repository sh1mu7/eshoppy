from django.urls import path, include
from rest_framework import routers
from .views import AdminDeliveryChargeAPI, AdminDeliveryRiderAPI

router = routers.DefaultRouter()
router.register('delivery_charge', AdminDeliveryChargeAPI)
router.register('rider', AdminDeliveryRiderAPI)

urlpatterns = [
    path('', include(router.urls))
]
