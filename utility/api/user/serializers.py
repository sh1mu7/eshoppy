from rest_framework import serializers

from ...models import GlobalSettings, Page, Currency, Banner, FAQ, SearchResult, EmailSubscription


class UserGlobalSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)

    class Meta:
        model = GlobalSettings
        fields = (
            'site_name', 'website_url', 'logo', 'email', 'phone', 'address', 'latitude', 'longitude', 'short_desc',
            'facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'logo_url'
        )


class UserPageListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(read_only=True, source='get_thumbnail_url')
    attachment_url = serializers.CharField(read_only=True, source='get_attachment_url')

    class Meta:
        model = Page
        fields = ('id', 'title', 'video_url', 'thumbnail_url', 'attachment_url', 'created_at')


class UserPageDetailsSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(read_only=True, source='get_thumbnail_url')
    attachment_url = serializers.CharField(read_only=True, source='get_attachment_url')

    class Meta:
        model = Page
        fields = '__all__'


class UserCurrencySerializer(serializers.ModelSerializer):
    currency_sign_url = serializers.CharField(source='get_currency_sign_url', read_only=True)

    class Meta:
        model = Currency
        fields = ('currency_name', 'currency_sign_url')


class UserBannerSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = Banner
        fields = ('id', 'name', 'image_url', 'expiry_date', 'position')


class UserFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'position')


class UserSearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = ('id', 'search_text',)


class UserEmailSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSubscription
        fields = ('email',)
