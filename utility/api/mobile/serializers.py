from rest_framework import serializers

from ...models import GlobalSettings, Page


class InfoSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(read_only=True, source='get_logo_url')

    class Meta:
        model = GlobalSettings
        fields = (
            'site_name', 'website_url', 'logo', 'email', 'phone', 'address', 'latitude', 'longitude', 'short_desc',
            'facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'logo_url'
        )


class PageListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(read_only=True, source='get_thumbnail_url')
    attachment_url = serializers.CharField(read_only=True, source='get_attachment_url')

    class Meta:
        model = Page
        fields = ('id', 'title', 'video_url', 'thumbnail_url', 'attachment_url', 'created_at')


class PageDetailsSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(read_only=True, source='get_thumbnail_url')
    attachment_url = serializers.CharField(read_only=True, source='get_attachment_url')

    class Meta:
        model = Page
        fields = '__all__'
