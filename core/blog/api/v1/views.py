from rest_framework.viewsets import ModelViewSet
from blog.models import Post
from blog.api.v1.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
