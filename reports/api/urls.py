from django.urls import path, include

urlpatterns = [
    path('admin/', include('reports.api.admin.urls'))
]
