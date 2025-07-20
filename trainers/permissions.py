from rest_framework import permissions

from users.models import Role


class IsAdminOrTrainerOwner(permissions.BasePermission):
    """
    Разрешает доступ только администраторам или владельцу профиля тренера.
    Клиенты могут просматривать список тренеров и отдельные профили.
    """

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user and request.user.is_staff
        if view.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if request.user and obj.user == request.user:
            return True
        if (
            request.user
            and request.user.role == Role.CLIENT
            and view.action == "retrieve"
        ):
            return True
        return False
