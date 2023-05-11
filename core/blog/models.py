from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    register_time = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)

    def __str__(self) -> str:
        return self.user.username
