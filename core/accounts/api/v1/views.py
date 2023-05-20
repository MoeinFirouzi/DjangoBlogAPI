from accounts.api.v1.serializers import (
    AuthTokenSerializer,
    UserRegisterSerializer,
    AuthorSerializer,
    ChangePasswordSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from django.contrib.auth import get_user_model
from accounts.models import Author
from rest_framework.permissions import IsAuthenticated
from accounts.api.v1.permissions import (
    SuperuserGetAuthenticatedPostPermission,
    SuperuserOrOwner,
)

User = get_user_model()


class CustomObtainAuthToken(ObtainAuthToken):
    """
    CustomObtainAuthToken is a class that extends the ObtainAuthToken class
    to provide a custom implementation for obtaining an authentication token.
    It uses the AuthTokenSerializer to validate user credentials and generate
    a token for the authenticated user.

    The post method is overridden to handle the authentication request.
    It takes in a request object, along with any additional arguments and
    keyword arguments, and returns a Response object containing the generated
    token, user ID, and email address.
    """

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id, "email": user.email})


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class CustomDiscardAuthToken(APIView):
    """
    This class represents an API view for discarding the authentication
    token of a user.

    Methods:
        post(request): Deletes the authentication token of the authenticated
        user and returns a response with status code 204.
    """

    permission_classes = [IsAuthenticated]

    def post(sef, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorRegister(ListCreateAPIView):
    """
    AuthorRegister is a view that allows authenticated users to register
    as authors. It uses the AuthorSerializer to create or retrieve an
    Author instance associated with the user making the request.
    If the user is already registered as an author, it raises
    a ValidationError. This view can only be accessed by authenticated
    users for POST requests and superusers for GET requests, as determined
    by the SuperuserGetAuthenticatedPostPermission permission class.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [SuperuserGetAuthenticatedPostPermission]


class AuthorDetail(RetrieveUpdateDestroyAPIView):
    """
    This class represents the view for retrieving, updating and
    deleting an Author object.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [SuperuserOrOwner]


class ChangePassword(GenericAPIView):
    """
    This module allows authenticated users to change their password.
    """

    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Handles PUT requests to change the user's password.
        Validates the request data,checks if old password is correct,
        sets new password and saves it. Returns a success or error response.

        """
        instance = self.get_object()
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
