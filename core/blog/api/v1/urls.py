from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.api.v1.views import PostViewSet

post_router = DefaultRouter()
post_router.register("post", PostViewSet, basename="post")

app_name = "api-v1"

urlpatterns = [
    path("", include(post_router.urls)),
]
