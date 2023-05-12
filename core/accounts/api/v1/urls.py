from django.urls import path, include
from accounts.api.v1.views import CustomObtainAuthToken, UserRegister

app_name = "account-api-v1"

urlpatterns = [
    path("login/", CustomObtainAuthToken.as_view(), name="user-login"),
    path("register/", UserRegister.as_view(), name="user-register"),
]
