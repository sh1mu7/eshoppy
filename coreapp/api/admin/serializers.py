from rest_framework import serializers
from coreapp.models import User


class UserListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'mobile', 'user_name', 'role')
