from django.urls import path, include
from rest_framework import routers

from cart.api.user.views import UserWishlistAPI, UserCartAPI

router = routers.DefaultRouter()
router.register('wishlist', UserWishlistAPI)
router.register('cart', UserCartAPI)

urlpatterns = [

]
urlpatterns += router.urls
