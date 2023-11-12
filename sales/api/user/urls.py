from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('address', views.CustomerAddressAPI)
router.register('reason', views.CustomerReasonAPI)
router.register('coupon', views.CustomerCouponAPI)
router.register('checkout', views.CustomerCheckoutAPI)

urlpatterns = [
    path('', include(router.urls))
]
