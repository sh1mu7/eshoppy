from django.urls import path, include
from rest_framework import routers
from .views import AdminOrderAPI

router = routers.DefaultRouter()
router.register('order', AdminOrderAPI)
urlpatterns = [
    path('', include(router.urls))
]
