from rest_framework import serializers

from ...models import GlobalSettings, Page, Payment, Currency, Banner, FAQ, SearchResult, Refund, EmailSubscription


class GlobalSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)

    class Meta:
        model = GlobalSettings
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    attachment_url = serializers.CharField(source='get_attachment_url', read_only=True)

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


class RefundListAdminSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(source='get_order_id')
    customer_name = serializers.CharField(source='get_customer_name')
    customer_phone = serializers.CharField(source='get_customer_phone')
    payment_id = serializers.CharField(source='get_payment_id')

    class Meta:
        model = Refund
        fields = (
            'id', 'order', 'order_id', 'payment', 'payment_id', 'customer_name', 'customer_phone',
            'refundable_amount', 'is_refunded', 'created_at'
        )


class AdminEmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ('id', 'email', 'is_active')
