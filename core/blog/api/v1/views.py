from rest_framework.viewsets import ModelViewSet
from blog.models import Post
from blog.api.v1.serializers import PostSerializer
from blog.api.v1.permissions import AuthorOrSuperuserWritePermission
from blog.api.v1.paginations import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class PostViewSet(ModelViewSet):
    """
    This class defines a view set for the Post model, which allows
    for CRUD operations on Post objects.

    Attributes:
    - queryset: A QuerySet containing all Post objects.
    - serializer_class: The serializer class used to serialize
    and deserialize Post objects.
    - permission_classes: A list of permission classes that determine
    whether a user has permission to perform certain actions on Post objects.
    In this case, the AuthorOrSuperuserWritePermission class is used, which
    allows authors and superusers to write (create, update, delete)
    Post objects.

    Methods:
    - Inherits all methods from the ModelViewSet class.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AuthorOrSuperuserWritePermission]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author"]
    search_fields = ["author__user__username", "title", "content"]
    ordering_fields = ["create_time"]
