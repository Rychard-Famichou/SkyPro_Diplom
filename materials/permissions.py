from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """Разрешения на объект для Авторов"""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "author", None) == request.user


class IsAdminRole(BasePermission):
    """Разрешения на объект для Администраторов"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "ADMIN")

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
