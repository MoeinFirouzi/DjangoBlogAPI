from django.urls import path, include
from accounts.api.v1.views import CustomObtainAuthToken

app_name = "account-api-v1"

urlpatterns = [
    path("login/", CustomObtainAuthToken.as_view(), name="user-login"),
]
