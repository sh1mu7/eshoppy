from django.urls import path, include

urlpatterns = [
    path('user/', include('cart.api.user.urls'))
]
