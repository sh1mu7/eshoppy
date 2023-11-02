from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from coreapp.base import BaseModel


# from coreapp.base import BaseModel


class Post(BaseModel):
    seo_title = models.CharField(max_length=60)
    seo_description = models.CharField(max_length=160)
    seo_keyword = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(editable=False, unique=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE)

    @cached_property
    def get_author_name(self):
        return self.author.get_full_name

    @cached_property
    def get_image_url(self):
        return self.image.get_url

    @cached_property
    def get_like_count(self):
        return self.post_like.count()

    @cached_property
    def get_comment_count(self):
        return self.post_comment.count()

    # @cached_property
    # def get_comments(self):
    #     return self.post_comment.all()

    def __str__(self):
        return self.title


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user')
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.user.get_full_name} on {self.post.title}'


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.get_full_name} likes {self.post.title}'
