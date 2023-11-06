from django.urls import path, include

urlpatterns = [
    path('admin/', include('sales.api.admin.urls')),
    path('user/', include('sales.api.user.urls'))
]
