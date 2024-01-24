from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('order', views.CustomerOrderAPI)
router.register('address', views.CustomerAddressAPI)
router.register('reason-type', views.CustomerReasonTypeAPI)
router.register('reason', views.CustomerReasonAPI)
router.register('coupon', views.CustomerCouponAPI)
router.register('checkout', views.CustomerCheckoutAPI)
router.register('return', views.CustomerOrderReturnAPI)

urlpatterns = [
    path('', include(router.urls))
]
