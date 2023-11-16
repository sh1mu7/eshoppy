from django.urls import path, include
from rest_framework import routers
from .views import RiderProfileAPI

router = routers.DefaultRouter()
router.register('profile', RiderProfileAPI)
urlpatterns = [
    path('', include(router.urls))
]
