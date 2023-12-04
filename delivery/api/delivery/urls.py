from django.urls import path, include
from rest_framework import routers
from .views import DeliveryManProfileAPI, RiderDeliveryRequestAPI, RiderOrderDeliveryAPI

router = routers.DefaultRouter()

router.register('delivery_request', RiderDeliveryRequestAPI)
router.register('delivery', RiderOrderDeliveryAPI)
router.register('profile', DeliveryManProfileAPI)
urlpatterns = [

]

urlpatterns += router.urls
