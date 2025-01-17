from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"refund", views.RefundAdminAPI)
router.register(r"page", views.PageAdminAPI)
router.register(r"currency", views.AdminCurrencyAPI)
router.register(r"banner", views.AdminBannerAPI)
router.register(r"faq", views.AdminFAQAPI)
router.register(r"search-result", views.AdminSearchResultAPI)
router.register(r"email-subscription", views.AdminEmailSubscriptionAPI)


urlpatterns = [
    path("global-settings/", views.GlobalSettingsAPI.as_view())
]
urlpatterns += router.urls
