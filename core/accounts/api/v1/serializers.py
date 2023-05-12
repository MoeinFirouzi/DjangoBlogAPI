from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Author

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        if User.objects.filter(email=validated_data.get("email")).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        user = User.objects.create_user(
            email=validated_data.get("email"),
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )

        return user


class AuthorSerializer(serializers.ModelSerializer):
    """
    This module contains a serializer for the Author model.

    def create(self, validated_data):
        This method creates a new Author instance with the given validated data.
        If an author with the same user already exists, it raises a validation error.
        Otherwise, it creates a new author with the given data and returns it.
    """

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        author, created = Author.objects.get_or_create(user=validated_data["user"])
        if created:
            author.company = validated_data["company"]
            author.address = validated_data["address"]
            author.save()

            return author

        else:
            raise serializers.ValidationError({"error": "Author already exists"})
