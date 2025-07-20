from rest_framework import permissions

from bookings.models import BookingStatus
from users.models import Role


class IsAdminOrClientOwnerOrTrainerOfSchedule(permissions.BasePermission):
    """
    Разрешает:
    - Администраторам: полный доступ.
    - Клиентам: просматривать свои записи, создавать новые, обновлять/отменять свои записи (только некоторые статусы).
    - Тренерам: просматривать записи на свои тренировки.
    """

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user and request.user.role == Role.CLIENT
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if request.user and request.user.role == Role.CLIENT:
            if obj.client == request.user:
                if view.action == "destroy":
                    return obj.status not in [
                        BookingStatus.COMPLETED,
                        BookingStatus.CANCELLED,
                    ]
                return True
            return False

        if request.user and request.user.role == Role.TRAINER:
            if obj.schedule.trainer.user == request.user:
                return view.action in ["retrieve", "list"]
            return False

        return False
