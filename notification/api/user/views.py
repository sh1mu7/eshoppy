from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from coreapp.permissions import IsCustomer, IsDeliveryStaff, IsAdminStaff
from . import serializers
from ...models import SystemAlert


class UserSystemAlertAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsCustomer | IsDeliveryStaff | IsAdminStaff]
    queryset = SystemAlert.objects.all()
    serializer_class = serializers.UserSystemAlertSerializer

    def get_queryset(self):
        queryset = SystemAlert.objects.filter(users=self.request.user)
        return queryset

    @extend_schema(request=serializers.IsReadSerializer)
    @action(detail=True, methods=['post'], url_path='is_read')
    def read_system_alert(self, request, pk=None):
        system_alert = SystemAlert.objects.get(id=pk)
        serializer = serializers.IsReadSerializer(data=request.data, instance=system_alert)
        serializer.is_valid(raise_exception=True)
        is_read = serializer.validated_data['is_read']
        system_alert.is_read = is_read
        system_alert.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='read_all')
    def read_all_system_alert(self):
        system_alert = SystemAlert.objects.filter(users=self.request.user)
        for alert in system_alert:
            alert.is_read = True
            alert.save()
        system_alert.save()
        return Response({'details': 'All alert are marked as read.'}, status=status.HTTP_200_OK)
