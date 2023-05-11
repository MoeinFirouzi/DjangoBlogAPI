from rest_framework import permissions
from blog.models import Author


class AuthorOrSuperuserWritePermission(permissions.BasePermission):
    """
    Allows access only to authenticated users who are either superusers
    or authors of the object being accessed.
    """

    def is_author(self, user):
        return Author.objects.filter(user=user.id).exists()

    def has_permission(self, request, view):
        """
        Returns True if the user is authenticated and is either a
        superuser or an author.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser or self.is_author(request.user)

    def has_object_permission(self, request, view, obj):
        """
        Returns True if the user is authenticated and is either a superuser
        or the author of the object being accessed.
        """
        if hasattr(obj, "author"):
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                if request.user.is_authenticated:
                    return (request.user.is_superuser) or (
                        obj.author.user == request.user
                    )

        return False
