from django.urls import path, include

urlpatterns = [
    path('admin/', include('reports.api.admin.urls')),
    path('rider/', include('reports.api.delivery.urls'))
]
