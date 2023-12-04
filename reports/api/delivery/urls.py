from django.urls import path, include
from . import views

urlpatterns = [
    path('delivery/statistics', views.DeliverStatisticsAPI.as_view())
]
