from django.urls import path, include

urlpatterns = [
    path('admin/', include('chat.api.admin.urls')),
    path('user/', include('chat.api.user.urls'))
]
