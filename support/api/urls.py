from django.urls import path, include

urlpatterns = [
    path('user/', include('support.api.user.urls')),
    path('admin/', include('support.api.admin.urls')),
]
