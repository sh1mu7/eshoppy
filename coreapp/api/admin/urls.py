from django.urls import path, include
from .views import UserAPI

urlpatterns = [
    path('', UserAPI.as_view())
]
