from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('package', views.UserPackageAPI)
router.register('subscription', views.UserSubscriptionAPI)

urlpatterns = [
    path('', include(router.urls))
]

