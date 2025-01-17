from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('brand', views.AdminBrandAPI)
router.register('category', views.AdminCategoryAPI)
router.register('variant-group', views.AdminVariantGroupAPI)
router.register('variant-option', views.AdminVariantOptionAPI)
router.register('product', views.AdminProductAPI)
router.register('promotion', views.AdminPromotionProductAPI)
router.register('productreview', views.AdminProductReviewAPI)

urlpatterns = [
    path('', include(router.urls))
]
