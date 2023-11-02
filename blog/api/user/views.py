from rest_framework.permissions import AllowAny

from coreapp.permissions import IsCustomer
from rest_framework import viewsets, mixins
from . import serializers
from ...models import Post, Comment, Like


class UserPostAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    queryset = Post.objects.all()
    serializer_class = serializers.UserPostSerializer


class UserCommentAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Comment.objects.all()
    serializer_class = serializers.UserCommentSerializer


class UserLikeAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsCustomer, ]
    queryset = Like.objects.all()
    serializer_class = serializers.UserLikeSerializer
