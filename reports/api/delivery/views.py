from coreapp.permissions import IsDeliveryStaff
from delivery.models import OrderDelivery
from delivery import constants
from django_filters import rest_framework as dj_filters
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework import views
from .. import filters


class DeliverStatisticsAPI(views.APIView):
    permission_classes = [IsDeliveryStaff, ]
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.DeliveryReportFilter

    def get(self, request):
        user = self.request.user
        delivery_counts = OrderDelivery.objects.filter(
            rider=user,
            rider_delivery_status__in=[
                constants.RiderOrderDeliveryStatus.ON_GOING,
                constants.RiderOrderDeliveryStatus.PICKED,
                constants.RiderOrderDeliveryStatus.ACTIVE,
                constants.RiderOrderDeliveryStatus.COMPLETED
            ]
        ).values('rider_delivery_status').annotate(count=Count('id'))
        data = {entry['rider_delivery_status']: entry['count'] for entry in delivery_counts}

        for status in [
            constants.RiderOrderDeliveryStatus.ON_GOING,
            constants.RiderOrderDeliveryStatus.PICKED,
            constants.RiderOrderDeliveryStatus.ACTIVE,
            constants.RiderOrderDeliveryStatus.COMPLETED
        ]:
            data.setdefault(status, 0)
        return Response(data)
