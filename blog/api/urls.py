from django.urls import path, include

urlpatterns = [
    path('admin/', include('blog.api.admin.urls')),
    path('public/', include('blog.api.user.urls'))
]
