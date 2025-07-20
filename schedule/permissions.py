from rest_framework import permissions

from users.models import Role


class IsAdminOrTrainerOwnerOfSchedule(permissions.BasePermission):
    """
    Разрешает доступ администраторам, или тренерам к своим расписаниям.
    Клиенты могут только просматривать расписания.
    """

    def has_permission(self, request, view):

        if view.action == "create":
            return request.user and (
                request.user.is_staff or request.user.role == Role.TRAINER
            )
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if (
            request.user
            and request.user.role == Role.TRAINER
            and obj.trainer.user == request.user
        ):
            return True
        if (
            request.user
            and request.user.role == Role.CLIENT
            and view.action == "retrieve"
        ):
            return True
        return False
