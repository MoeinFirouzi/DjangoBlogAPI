import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User,Author
client = APIClient()

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def test_user():
    user = User.objects.create_user(email="moein@gmail.com", password="12/2@moein")
    author = Author.objects.create(user=user)
    return user

@pytest.mark.django_db
class TestPostAPI:
    
    def test_get_post_response_200(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_post_post_response_401(self,api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test-title",
            "content": "test-content",
            "status": False
        }
        response = api_client.post(url,data)
        assert response.status_code == 401
        
        
    def test_post_post_response_201(self,api_client, test_user):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test-title",
            "content": "test-content",
            "status": False
        }
        user = test_user
        api_client.force_login(user=user)
        response = api_client.post(url,data)
        assert response.status_code == 201