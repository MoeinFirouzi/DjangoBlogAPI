from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Author
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})
