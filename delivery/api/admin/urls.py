from django.urls import path, include
from rest_framework import routers
from .views import AdminDeliveryChargeAPI

router = routers.DefaultRouter()
router.register('delivery_charge', AdminDeliveryChargeAPI)

urlpatterns = [
    path('', include(router.urls))
]
