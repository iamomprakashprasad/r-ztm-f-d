from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner can access their own task; admin can access any."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj.owner == request.user


class IsAdminRole(BasePermission):
    """View-level: only users with role='admin' are allowed."""

    message = "Access restricted to admin users only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")
