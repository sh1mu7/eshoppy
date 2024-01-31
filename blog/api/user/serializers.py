from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blog.models import Comment, Post, Like


class UserCommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'comment_author', 'post', 'created_at')
        read_only_fields = ('user',)

    def create(self, validated_data):
        comment_author = self.context['request'].user
        validated_data['user'] = comment_author
        return Comment.objects.create(**validated_data)


class UserPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    like_count = serializers.IntegerField(source='get_like_count', read_only=True)
    comment_count = serializers.IntegerField(source='get_comment_count', read_only=True)
    image_url = serializers.CharField(source='get_image_url', read_only=True)
    post_comment = UserCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'post_comment',)

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        return Post.objects.create(**validated_data)


class UserLikeSerializer(serializers.ModelSerializer):
    liked_user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Like
        fields = ('liked_user', 'post', 'is_like')

    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data['post']
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError({"User": ["You have already liked this post."]})
        like = Like.objects.create(user=user, **validated_data)
        return like
