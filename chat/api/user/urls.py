from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('message', views.UserMessageAPI)

urlpatterns = [

]
urlpatterns += router.urls
