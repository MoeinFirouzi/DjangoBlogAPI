from accounts.api.v1.serializers import (
    AuthTokenSerializer,
    UserRegisterSerializer,
    AuthorSerializer,
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
