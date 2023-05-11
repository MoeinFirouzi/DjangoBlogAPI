from django.urls import path, include


app_name = "account"

urlpatterns = [
    path("api/v-1/", include("accounts.api.v1.urls")),
]
