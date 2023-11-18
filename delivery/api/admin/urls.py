from django.urls import path, include
from rest_framework import routers
from .views import AdminOrderAPI, AdminDeliveryChargeAPI

router = routers.DefaultRouter()
router.register('order', AdminOrderAPI)
router.register('delivery_charge', AdminDeliveryChargeAPI)

urlpatterns = [
    path('', include(router.urls))
]
