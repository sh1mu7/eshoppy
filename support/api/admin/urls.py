from rest_framework import routers
from .views import AdminTicketReplyAPI, AdminSupportTicketAPI

router = routers.DefaultRouter()
router.register('ticket', AdminSupportTicketAPI)
router.register('reply', AdminTicketReplyAPI)

urlpatterns = [

]
urlpatterns += router.urls
