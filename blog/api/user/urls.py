from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('post', views.UserPostAPI)
router.register('comment', views.UserCommentAPI)
router.register('like', views.UserLikeAPI)

urlpatterns = [
    path('', include(router.urls))
]
