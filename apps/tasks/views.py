from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrAdmin
from .pagination import TaskPagination


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["completed"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        return Task.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of tasks. Admins see all tasks; regular users see only their own. Filter by `completed`, search by `title` or `description`.",
        manual_parameters=[
            openapi.Parameter("completed", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Filter by completion status"),
            openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search in title and description"),
            openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Page number"),
            openapi.Parameter("page_size", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Number of results per page"),
        ],
        tags=["Tasks"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new task. The task is automatically assigned to the authenticated user.",
        request_body=TaskSerializer,
        responses={201: TaskSerializer},
        tags=["Tasks"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        return Task.objects.filter(owner=user)

    @swagger_auto_schema(
        operation_description="Retrieve a single task by ID.",
        responses={200: TaskSerializer, 404: "Not Found"},
        tags=["Tasks"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Fully update a task. Only the owner or an admin can do this.",
        request_body=TaskSerializer,
        responses={200: TaskSerializer},
        tags=["Tasks"],
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a task. Only the owner or an admin can do this.",
        request_body=TaskSerializer,
        responses={200: TaskSerializer},
        tags=["Tasks"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a task. Only the owner or an admin can do this.",
        responses={204: "Deleted successfully"},
        tags=["Tasks"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
