from accounts.api.v1.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


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
