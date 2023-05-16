from django.urls import path, include
from accounts.api.v1.views import (
    CustomObtainAuthToken,
    UserRegister,
    AuthorRegister,
    AuthorDetail)

app_name = "account-api-v1"

urlpatterns = [
    path("login/", CustomObtainAuthToken.as_view(), name="user-login"),
    path("register/", UserRegister.as_view(), name="user-register"),
    path("register-author/", AuthorRegister.as_view(), name="author-register"),
    path("author/<int:pk>/", AuthorDetail.as_view(), name="author-detail"),
]
