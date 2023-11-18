from rest_framework import serializers
from ...models import SystemAlert


class UserSystemAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAlert
        fields = ('id', 'title', 'message', 'is_read')


class IsReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField(default=True)
