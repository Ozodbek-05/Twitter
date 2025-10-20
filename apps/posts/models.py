from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuthorModel(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_profile'
    )
    avatar = models.CharField(max_length=2)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

class FollowModel(BaseModel):
    follower = models.ForeignKey(AuthorModel, related_name='following_relations', on_delete=models.CASCADE)
    following = models.ForeignKey(AuthorModel, related_name='follower_relations', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)


class PostModel(BaseModel):
    message = models.TextField()
    author = models.ForeignKey(
        AuthorModel,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    likes = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.user.username} - {self.message[:20]}"

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class CommentModel(BaseModel):
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        AuthorModel,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.user.username}: {self.text[:30]}"

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
