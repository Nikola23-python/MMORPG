from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    code = models.CharField(max_length=10, )

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('merchants', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=12)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)