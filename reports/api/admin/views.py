from rest_framework import views, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from coreapp.models import User
from inventory.models import Product, Category
from sales import constants
from sales.models import Order
from subscription.models import Package


class DashboardInformationAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self):
        total_user = User.objects.filter(role=2).all()
        total_rider = User.objects.filter(role=3).all()
        total_package = Package.objects.filter(is_active=True).all()
        total_products = Product.objects.filter(is_active=True).all()
        total_category = Category.objects.filter(is_active=True).all()
        total_order = Order.objects.all()
        total_pending_order = Order.objects.filter(order_status=constants.OrderStatus.PENDING).all()
        total_completed_order = Order.objects.filter(order_status=constants.OrderStatus.DELIVERED).all()
        total_cancelled_order = Order.objects.filter(order_status=constants.OrderStatus.CANCELED).all()

        data = {
            'total_user': total_user,
            'total_rider': total_rider,
            'total_package': total_package,
            'total_products': total_products,
            'total_category': total_category,
            'total_order': total_order,
            'total_pending_order': total_pending_order,
            'total_completed_order': total_completed_order,
            'total_cancelled_order': total_cancelled_order,
        }

        return Response(data, status=status.HTTP_200_OK)
