from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('auth/', include('coreapp.api.urls')),
    path('chat/', include('chat.api.urls')),
    path('inventory/', include('inventory.api.urls')),
    path('cart/', include('cart.api.urls')),
    path('sales/', include('sales.api.urls')),
    path('delivery/', include('delivery.api.urls')),
    path('package/', include('subscription.api.urls')),
    path('reports/', include('reports.api.urls')),
    path('notification/', include('notification.api.urls')),
    # path('utility/', include('utility.api.urls')),
    path('utility/', include('utility.urls')),
    path('support/', include('support.api.urls')),
    path('blog/', include('blog.api.urls')),
]
