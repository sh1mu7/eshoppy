from django.urls import path, include

urlpatterns = [
    path("mobile/", include("utility.api.mobile.urls")),
    path("user/", include("utility.api.user.urls")),
    path("admin/", include("utility.api.admin.urls"))
]
