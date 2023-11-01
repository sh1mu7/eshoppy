from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('brand', views.CustomerBrandAPI)
router.register('category', views.CustomerCategoryAPI)

urlpatterns = [
    path('', include(router.urls))
]
