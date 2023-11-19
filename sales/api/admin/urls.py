from django.urls import path, include
from rest_framework import routers
from .views import AdminCouponAPI, AdminReasonAPI,AdminOrderAPI

router = routers.DefaultRouter()

router.register('order', AdminOrderAPI)
router.register('reason', AdminReasonAPI)
router.register('coupon', AdminCouponAPI)

urlpatterns = [
    path('', include(router.urls))
]
