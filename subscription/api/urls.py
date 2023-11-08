from django.urls import path, include

urlpatterns = [
    path('admin/', include('subscription.api.admin.urls')),
    path('user/', include('subscription.api.user.urls'))
]
