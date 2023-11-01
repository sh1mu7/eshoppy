from django.urls import path, include

urlpatterns = [
    path('admin/', include('blog.api.admin.urls'))
]
