from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('package', views.AdminPackageAPI)
router.register('customer-info', views.CustomerInformationAPI)
router.register('subscription', views.AdminSubscriptionAPI)

urlpatterns = [
    path('', include(router.urls))
]
