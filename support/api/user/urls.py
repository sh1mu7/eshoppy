from rest_framework import routers
from .views import UserSupportTicketAPI

router = routers.DefaultRouter()
router.register('ticket', UserSupportTicketAPI)

urlpatterns = [

]
urlpatterns += router.urls
