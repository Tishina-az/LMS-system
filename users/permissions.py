from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяем, состоит ли пользователь в группе 'Модератор'."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модератор").exists()
