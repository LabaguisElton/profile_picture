from django.db import models
from django.contrib.auth.models import User


class Account(User):
    class Meta:
        proxy = True
        verbose_name = 'account'
        verbose_name_plural = 'accounts'


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
    )
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:30]}'


class PageProfile(models.Model):
    image = models.ImageField(upload_to='profile_pictures/', blank=True)
