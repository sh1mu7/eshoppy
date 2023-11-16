from django.db.models import Count
from rest_framework import views, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from coreapp.models import User
from inventory.models import Product, Category
from sales import constants
from sales.models import Order
from subscription.models import Package, SubscriptionHistory


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('invoice_no', 'customer', 'order_status', 'total')


class DashboardInformationAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        total_user = User.objects.filter(role=2).count()
        total_rider = User.objects.filter(role=3).count()
        total_package = Package.objects.filter(is_active=True).count()
        total_active_subscriber = SubscriptionHistory.objects.filter(is_expired=False).count()
        total_subscriber = SubscriptionHistory.objects.values('customer').annotate(total_subscriber=Count('id'))
        total_products = Product.objects.filter(is_active=True).count()
        total_category = Category.objects.filter(is_active=True).count()
        total_order = Order.objects.all().count()
        recent_orders = Order.objects.all().order_by('-id')[:10]
        total_pending_order = Order.objects.filter(order_status=constants.OrderStatus.PENDING).count()
        total_completed_order = Order.objects.filter(order_status=constants.OrderStatus.DELIVERED).count()
        total_cancelled_order = Order.objects.filter(order_status=constants.OrderStatus.CANCELED).count()
        recent_orders_data = OrderSerializer(recent_orders, many=True).data

        data = {
            'total_user': total_user,
            'total_rider': total_rider,
            'total_package': total_package,
            'total_active_subscriber': total_active_subscriber,
            'total_subscriber': total_subscriber,
            'total_products': total_products,
            'total_category': total_category,
            'total_order': total_order,
            'total_pending_order': total_pending_order,
            'total_completed_order': total_completed_order,
            'total_cancelled_order': total_cancelled_order,
            'recent_orders': recent_orders_data,
        }

        return Response(data, status=status.HTTP_200_OK)
