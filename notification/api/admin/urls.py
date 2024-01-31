from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(r'notifications', views.AdminNotificationAPI)
urlpatterns = [
    path('fcm/', views.AdminFCMNotificationAPI.as_view()),

]
urlpatterns += router.urls
