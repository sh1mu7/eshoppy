from rest_framework import serializers

from ...models import GlobalSettings, Page, Payment, Currency, Banner, FAQ, SearchResult


class GlobalSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)

    class Meta:
        model = GlobalSettings
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)

    class Meta:
        model = Page
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class AdminCurrencySerializer(serializers.ModelSerializer):
    currency_sign_url = serializers.CharField(source='get_currency_sign_url', read_only=True)

    class Meta:
        model = Currency
        fields = "__all__"


class AdminBannerSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = Banner
        fields = "__all__"


class AdminFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class AdminSearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = "__all__"
