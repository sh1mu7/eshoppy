from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from . import serializers
from ...models import Post, Comment, Like


class AdminPostAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Post.objects.all()
    serializer_class = serializers.AdminPostSerializer


class AdminCommentAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Comment.objects.all()
    serializer_class = serializers.AdminCommentSerializer


class AdminLikeAPI(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Like.objects.all()
    serializer_class = serializers.AdminLikeSerializer
