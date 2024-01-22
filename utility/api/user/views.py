from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as dj_filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, views, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from coreapp.permissions import IsCustomer
from coreapp.utils.auth_utils import get_client_info
from . import serializers
from ... import constants
from ...models import GlobalSettings, Page, Currency, Banner, FAQ, SearchResult, EmailSubscription


class InfoAPI(views.APIView):
    permission_classes = [AllowAny, ]

    @extend_schema(
        responses={200: serializers.UserGlobalSettingsSerializer}
    )
    def get(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.UserGlobalSettingsSerializer(global_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PageReadOnlyAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Page.objects.filter(is_active=True)
    serializer_class = serializers.UserPageListSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_fields = ('page_type',)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.UserPageDetailsSerializer
        return self.serializer_class

    @extend_schema(
        responses={200: serializers.UserPageDetailsSerializer}
    )
    @action(detail=True, methods=['get'], url_path='fixed-page')
    def fixed_page(self, request, pk=None):
        page = Page.objects.filter(page_type=pk, is_active=True).first()
        if page:
            serializer = serializers.UserPageDetailsSerializer(page)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": _("Page not found")}, status=status.HTTP_404_NOT_FOUND)


class CurrencyReadOnlyAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = serializers.UserCurrencySerializer


class BannerReadOnlyAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Banner.objects.filter(is_active=True).order_by('position')
    serializer_class = serializers.UserBannerSerializer


class FAQReadOnlyAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = serializers.UserFAQSerializer

    def get_queryset(self):
        queryset = FAQ.objects.filter(faq_type=constants.FaqType.Customer)
        return queryset


class SearchResultAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = SearchResult.objects.all()
    serializer_class = serializers.UserSearchResultSerializer

    def get_queryset(self):
        queryset = SearchResult.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
        ip, user_agent = get_client_info(self.request)
        serializer.save(user_agent=user_agent, ip_address=ip, user=self.request.user)


class UserEmailSubscriptionAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    queryset = EmailSubscription.objects.all()
    serializer_class = serializers.UserEmailSubscriptionSerializer
