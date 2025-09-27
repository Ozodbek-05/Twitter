from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthorModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'


class PostModel(BaseModel):
    message = models.TextField()
    author = models.ForeignKey(
        AuthorModel,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return f"{self.author.user.username} - {self.message[:20]}"

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

