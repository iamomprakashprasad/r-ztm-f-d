import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(email="user@example.com", username="testuser", password="strongpass123", role="user"):
        return User.objects.create_user(
            email=email,
            username=username,
            password=password,
            role=role,
        )
    return make_user


@pytest.fixture
def create_admin(db):
    def make_admin(email="admin@example.com", username="adminuser", password="adminpass123"):
        return User.objects.create_user(
            email=email,
            username=username,
            password=password,
            role="admin",
        )
    return make_admin


@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    response = api_client.post(
        "/api/auth/login/",
        {"email": "user@example.com", "password": "strongpass123"},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    api_client._user = user
    return api_client


@pytest.fixture
def admin_client(api_client, create_admin):
    admin = create_admin()
    response = api_client.post(
        "/api/auth/login/",
        {"email": "admin@example.com", "password": "adminpass123"},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    api_client._user = admin
    return api_client
