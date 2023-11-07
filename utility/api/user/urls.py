from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"page", views.PageReadOnlyAPI)
router.register(r"currency", views.CurrencyReadOnlyAPI)
router.register(r"banner", views.BannerReadOnlyAPI)
router.register(r"faq", views.FAQReadOnlyAPI)
router.register(r"search-result", views.SearchResultAPI)

urlpatterns = [
    path("info/", views.InfoAPI.as_view()),
    path("", include(router.urls)),
]
