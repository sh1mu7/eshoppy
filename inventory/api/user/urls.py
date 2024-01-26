from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('brand', views.CustomerBrandAPI)
router.register('category', views.CustomerCategoryAPI)
router.register('product', views.CustomerProductAPI)
router.register('productreview', views.CustomerProductReviewAPI)
router.register('top-selling', views.TopSellingProduct)

urlpatterns = [
    path('', include(router.urls))
]
