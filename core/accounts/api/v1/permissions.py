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
