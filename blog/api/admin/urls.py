from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('post', views.AdminPostAPI)
router.register('comment', views.AdminCommentAPI)
router.register('like', views.AdminLikeAPI)

urlpatterns = [
    path('', include(router.urls))
]
