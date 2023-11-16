from django.urls import path, include

urlpatterns = [
    path('rider/', include('delivery.api.delivery.urls')),
    path('admin/', include('delivery.api.admin.urls'))
]
