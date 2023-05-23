from rest_framework import permissions


class SuperuserGetAuthenticatedPostPermission(permissions.BasePermission):
    """
    Permission class that allows superusers to perform
    GET requests and authenticated users to perform POST requests.
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_superuser

        elif request.method == "POST":
            return request.user.is_authenticated

        return False


class SuperuserOrOwner(permissions.BasePermission):
    """
    SuperuserOrOwner allows access to an object only if the user making
    the request is either a superuser or the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user == obj.user) or (request.user.is_superuser)
        else:
            return request.user == obj.user
