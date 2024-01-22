from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from coreapp import roles
from coreapp.api.admin.serializers import UserListSerializer
from coreapp.models import User


class UserAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(Q(role=roles.UserRoles.CUSTOMER) | Q(role=roles.UserRoles.DELIVERY_STAFF))
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
