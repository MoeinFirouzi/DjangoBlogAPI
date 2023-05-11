from django.urls import path, include

app_name = "blog"

urlpatterns = [
    path('api/v-1/',include('blog.api.v1.urls')),
]
