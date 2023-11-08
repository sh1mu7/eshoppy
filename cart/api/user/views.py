from rest_framework import viewsets, mixins
from . import serializers
from coreapp.permissions import IsCustomer
from ...models import Wishlist, Cart


class UserWishlistAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Wishlist.objects.all()
    serializer_class = serializers.UserWishlistListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Wishlist.objects.filter(user=user).order_by('-created_at')
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserWishlistCreateSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super(UserWishlistAPI, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class UserCartAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Cart.objects.all()
    serializer_class = serializers.UserCartListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by('-created_at')
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCartCreateSerializer
        elif self.action == 'update':
            return serializers.UserCartUpdateSerializer
        return self.serializer_class
