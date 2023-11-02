from rest_framework import serializers
from ...models import Post, Comment, Like


class AdminCommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        comment_author = self.context['request'].user
        validated_data['user'] = comment_author
        return Comment.objects.create(**validated_data)


class AdminPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    like_count = serializers.CharField(source='get_like_count', read_only=True)
    image_url = serializers.CharField(source='get_image_url', read_only=True)
    post_comment = AdminCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'post_comment',)

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        return Post.objects.create(**validated_data)


class AdminLikeSerializer(serializers.ModelSerializer):
    liked_user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)
