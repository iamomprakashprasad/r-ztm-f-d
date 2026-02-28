import pytest


@pytest.mark.django_db
class TestRegister:
    def test_register_success(self, api_client):
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 201
        assert response.data["email"] == "new@example.com"
        assert "password" not in response.data

    def test_register_duplicate_email(self, api_client, create_user):
        create_user(email="dup@example.com", username="existing")
        payload = {
            "username": "someone",
            "email": "dup@example.com",
            "password": "securepass123",
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400

    def test_register_short_password(self, api_client):
        payload = {
            "username": "someone",
            "email": "short@example.com",
            "password": "123",
        }
        response = api_client.post("/api/auth/register/", payload, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, create_user):
        create_user(email="login@example.com", username="loginuser", password="loginpass123")
        response = api_client.post(
            "/api/auth/login/",
            {"email": "login@example.com", "password": "loginpass123"},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, create_user):
        create_user(email="wp@example.com", username="wpuser", password="correctpass")
        response = api_client.post(
            "/api/auth/login/",
            {"email": "wp@example.com", "password": "wrongpass"},
            format="json",
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post(
            "/api/auth/login/",
            {"email": "ghost@example.com", "password": "anything"},
            format="json",
        )
        assert response.status_code == 401
