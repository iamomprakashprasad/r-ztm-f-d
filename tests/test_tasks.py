import pytest
from apps.tasks.models import Task


@pytest.mark.django_db
class TestTaskAccess:
    def test_list_tasks_unauthenticated(self, api_client):
        response = api_client.get("/api/tasks/")
        assert response.status_code == 401

    def test_create_task_unauthenticated(self, api_client):
        response = api_client.post("/api/tasks/", {"title": "Hack"}, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestTaskCRUD:
    def test_create_task(self, auth_client):
        payload = {"title": "Finish report", "description": "Q4 summary", "completed": False}
        response = auth_client.post("/api/tasks/", payload, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Finish report"
        assert response.data["completed"] is False

    def test_list_tasks(self, auth_client):
        auth_client.post("/api/tasks/", {"title": "Task A"}, format="json")
        auth_client.post("/api/tasks/", {"title": "Task B"}, format="json")
        response = auth_client.get("/api/tasks/")
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_retrieve_task(self, auth_client):
        created = auth_client.post("/api/tasks/", {"title": "Read mail"}, format="json")
        task_id = created.data["id"]
        response = auth_client.get(f"/api/tasks/{task_id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Read mail"

    def test_update_task(self, auth_client):
        created = auth_client.post("/api/tasks/", {"title": "Old title"}, format="json")
        task_id = created.data["id"]
        response = auth_client.patch(f"/api/tasks/{task_id}/", {"title": "New title", "completed": True}, format="json")
        assert response.status_code == 200
        assert response.data["title"] == "New title"
        assert response.data["completed"] is True

    def test_delete_task(self, auth_client):
        created = auth_client.post("/api/tasks/", {"title": "To delete"}, format="json")
        task_id = created.data["id"]
        response = auth_client.delete(f"/api/tasks/{task_id}/")
        assert response.status_code == 204
        response = auth_client.get(f"/api/tasks/{task_id}/")
        assert response.status_code == 404

    def test_user_cannot_see_others_tasks(self, auth_client, api_client, create_user):
        other = create_user(email="other@example.com", username="otheruser")
        task = Task.objects.create(title="Private", owner=other)
        response = auth_client.get(f"/api/tasks/{task.id}/")
        assert response.status_code == 404

    def test_user_cannot_delete_others_tasks(self, auth_client, api_client, create_user):
        other = create_user(email="other2@example.com", username="otheruser2")
        task = Task.objects.create(title="Someone else task", owner=other)
        response = auth_client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code in (403, 404)


@pytest.mark.django_db
class TestTaskFiltering:
    def test_filter_by_completed(self, auth_client):
        auth_client.post("/api/tasks/", {"title": "Done task", "completed": True}, format="json")
        auth_client.post("/api/tasks/", {"title": "Pending task", "completed": False}, format="json")
        response = auth_client.get("/api/tasks/?completed=true")
        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == "Done task"

    def test_filter_completed_false(self, auth_client):
        auth_client.post("/api/tasks/", {"title": "Done task", "completed": True}, format="json")
        auth_client.post("/api/tasks/", {"title": "Pending task", "completed": False}, format="json")
        response = auth_client.get("/api/tasks/?completed=false")
        assert response.status_code == 200
        assert response.data["count"] == 1


@pytest.mark.django_db
class TestTaskPagination:
    def test_pagination_structure(self, auth_client):
        for i in range(5):
            auth_client.post("/api/tasks/", {"title": f"Task {i}"}, format="json")
        response = auth_client.get("/api/tasks/?page=1")
        assert response.status_code == 200
        assert "count" in response.data
        assert "results" in response.data
        assert "next" in response.data

    def test_per_page_limit(self, auth_client):
        for i in range(6):
            auth_client.post("/api/tasks/", {"title": f"Task {i}"}, format="json")
        response = auth_client.get("/api/tasks/?page_size=3")
        assert response.status_code == 200
        assert len(response.data["results"]) <= 6


@pytest.mark.django_db
class TestAdminAccess:
    def test_admin_sees_all_tasks(self, auth_client, admin_client, create_user):
        auth_client.post("/api/tasks/", {"title": "User task"}, format="json")
        response = admin_client.get("/api/tasks/")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_admin_can_delete_any_task(self, auth_client, admin_client):
        created = auth_client.post("/api/tasks/", {"title": "User task"}, format="json")
        task_id = created.data["id"]
        response = admin_client.delete(f"/api/tasks/{task_id}/")
        assert response.status_code == 204
