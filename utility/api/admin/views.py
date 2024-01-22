from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, views, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from . import serializers
from ...models import GlobalSettings, Page, Currency, FAQ, Banner, SearchResult, Refund, EmailSubscription


class GlobalSettingsAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer}
    )
    def get(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(global_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer},
        request=serializers.GlobalSettingsSerializer
    )
    def post(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(data=request.data, instance=global_settings)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefundAdminAPI(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Refund.objects.all()
    serializer_class = serializers.RefundListAdminSerializer

    # filter_backends = [dj_filters.DjangoFilterBackend]
    # filterset_class = filters.RefundAdminFilter

    @extend_schema(request=False)
    @action(detail=True, methods=['get'], url_path='make_refund')
    def make_refund(self, request, pk=None):
        refund = Refund.objects.get(id=pk)
        if refund.is_refunded is True:
            return Response({'detail': 'Refund already completed.'})
        refund.is_refunded = True
        refund.save()
        return Response({'detail': 'Refunded Successfully.'})


class PageAdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer


class AdminCurrencyAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Currency.objects.all()
    serializer_class = serializers.AdminCurrencySerializer


class AdminBannerAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Banner.objects.all()
    serializer_class = serializers.AdminBannerSerializer


class AdminFAQAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = FAQ.objects.all()
    serializer_class = serializers.AdminFAQSerializer


class AdminSearchResultAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAdminUser, ]
    queryset = SearchResult.objects.all()
    serializer_class = serializers.AdminSearchResultSerializer


class AdminEmailSubscriptionAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    queryset = EmailSubscription.objects.all()
    serializer_class = serializers.AdminEmailSubscriptionSerializer
