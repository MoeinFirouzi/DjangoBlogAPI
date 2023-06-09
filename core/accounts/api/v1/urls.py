from django.urls import path
from accounts.api.v1.views import (
    CustomObtainAuthToken,
    UserRegister,
    AuthorRegister,
    AuthorDetail,
    CustomDiscardAuthToken,
    ChangePassword,
)

app_name = "account-api-v1"

urlpatterns = [
    path("login/", CustomObtainAuthToken.as_view(), name="user-login"),
    path("register/", UserRegister.as_view(), name="user-register"),
    path("logout/", CustomDiscardAuthToken.as_view(), name="user-logout"),
    path("author/", AuthorRegister.as_view(), name="author-register"),
    path("author/<int:pk>/", AuthorDetail.as_view(), name="author-detail"),
    path(
        "change_password/",
        ChangePassword.as_view(),
        name="change-user-password",
    ),
]
