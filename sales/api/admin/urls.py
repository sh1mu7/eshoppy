from django.urls import path, include
from rest_framework import routers
from .views import AdminCouponAPI, AdminReasonAPI

router = routers.DefaultRouter()
router.register('reason', AdminReasonAPI)
router.register('coupon', AdminCouponAPI)

urlpatterns = [
    path('', include(router.urls))
]
