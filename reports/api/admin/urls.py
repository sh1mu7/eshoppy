from django.urls import path, include
from . import views

urlpatterns = [
    path('info', views.DashboardInformationAPI.as_view())
]
