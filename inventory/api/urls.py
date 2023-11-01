from django.urls import path, include

urlpatterns = [
    path('admin/', include('inventory.api.admin.urls')),
    path('customer/', include('inventory.api.user.urls')),
]
