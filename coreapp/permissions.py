from rest_framework.permissions import BasePermission
from .roles import UserRoles


class IsAdminStaff(BasePermission):
    """
    Allows access only AdminStaff
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.ADMIN_STAFF)


class IsCustomer(BasePermission):
    """
    Allows access only Customer
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.CUSTOMER)


class IsDeliveryStaff(BasePermission):
    """
    Allows access only DeliveryStaff
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.DELIVERY_STAFF)
