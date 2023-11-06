from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('auth/', include('coreapp.api.urls')),
    path('inventory/', include('inventory.api.urls')),
    path('sales/', include('sales.api.urls')),
    path('utility/', include('utility.api.urls')),
    path('blog/', include('blog.api.urls')),

]
