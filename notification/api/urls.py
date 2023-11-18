from django.urls import path, include

urlpatterns = [
    path('admin/', include('notification.api.admin.urls')),
    path('user/', include('notification.api.user.urls'))
]
