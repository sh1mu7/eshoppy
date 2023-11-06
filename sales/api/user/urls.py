from django.urls import path, include
from rest_framework import routers

from .views import CustomerAddressAPI, CustomerReasonAPI, CustomerCouponAPI

router = routers.DefaultRouter()
router.register('address', CustomerAddressAPI)
router.register('reason', CustomerReasonAPI)
router.register('coupon', CustomerCouponAPI)

urlpatterns = [
    path('', include(router.urls))
]
