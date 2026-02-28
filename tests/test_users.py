import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserRoles:
    def test_admin_can_list_users(self, admin_client, create_user):
        create_user(email="regular@example.com", username="regularuser")
        response = admin_client.get("/api/auth/users/")
        assert response.status_code == 200
        assert response.data["count"] >= 2  # admin + regular user

    def test_regular_user_cannot_list_users(self, auth_client):
        response = auth_client.get("/api/auth/users/")
        assert response.status_code == 403

    def test_unauthenticated_cannot_list_users(self, api_client):
        response = api_client.get("/api/auth/users/")
        # JWT auth returns 401 before the IsAdminRole permission check (403).
        # Both mean access is denied to unauthenticated callers.
        assert response.status_code in (401, 403)

    def test_user_list_contains_role_field(self, admin_client):
        response = admin_client.get("/api/auth/users/")
        assert response.status_code == 200
        if response.data["results"]:
            assert "role" in response.data["results"][0]
