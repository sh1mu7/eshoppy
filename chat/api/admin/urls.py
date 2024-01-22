from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('message', views.AdminMessageAPI)

urlpatterns = [

]
urlpatterns += router.urls
