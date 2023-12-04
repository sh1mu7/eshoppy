from rest_framework.serializers import ModelSerializer
from ...models import SystemAlert, PersonalNotification


class AdminSystemAlertSerializer(ModelSerializer):
    class Meta:
        model = SystemAlert
        fields = '__all__'

    def create(self, validated_data):
        users = validated_data.pop('users')
        system_alert = SystemAlert.objects.create(**validated_data)
        system_alert.users.set(users)
        system_alert.save()
        return system_alert


class AdminPersonalNotificationSerializer(ModelSerializer):
    class Meta:
        model = PersonalNotification
        fields = '__all__'


