from rest_framework import viewsets, permissions as drf_permissions
from .models import Booking, BookingStatus
from . import permissions as local_permissions
from .serializers import BookingSerializer
from users.models import Role
from .schemas import booking_extend_schema_view


@booking_extend_schema_view
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-booking_date", "-booking_time")
    serializer_class = BookingSerializer
    permission_classes = [local_permissions.IsAdminOrClientOwnerOrTrainerOfSchedule]

    def get_queryset(self):
        queryset = super().get_queryset()

        if (
            self.request.user.is_authenticated
            and self.request.user.role == Role.CLIENT
            and not self.request.user.is_staff
        ):
            queryset = queryset.filter(client=self.request.user)
        elif (
            self.request.user.is_authenticated
            and self.request.user.role == Role.TRAINER
            and not self.request.user.is_staff
        ):
            queryset = queryset.filter(schedule__trainer__user=self.request.user)

        schedule_id = self.request.query_params.get("schedule_id")
        if schedule_id:
            queryset = queryset.filter(schedule__id=schedule_id)

        booking_date = self.request.query_params.get("booking_date")
        if booking_date:
            queryset = queryset.filter(booking_date=booking_date)

        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def perform_create(self, serializer):

        if self.request.user.role == Role.CLIENT:
            serializer.save(client=self.request.user)
        else:
            serializer.save()

    def perform_update(self, serializer):

        if self.request.user.role == Role.CLIENT and not self.request.user.is_staff:
            if serializer.instance.client != self.request.user:
                raise drf_permissions.PermissionDenied(
                    "Вы можете обновлять только свои записи."
                )
            if (
                "status" in serializer.validated_data
                and serializer.validated_data["status"] != BookingStatus.CANCELLED
            ):
                raise drf_permissions.PermissionDenied(
                    "Вы можете только отменить свою запись."
                )

            if serializer.instance.status in [
                BookingStatus.COMPLETED,
                BookingStatus.CANCELLED,
            ]:
                raise drf_permissions.PermissionDenied(
                    f"Невозможно изменить статус записи, которая уже '{serializer.instance.get_status_display()}'."
                )
        serializer.save()

    def perform_destroy(self, instance):

        if self.request.user.is_staff:
            instance.delete()
        elif (
            self.request.user.role == Role.CLIENT
            and instance.client == self.request.user
        ):
            if instance.status not in [
                BookingStatus.COMPLETED,
                BookingStatus.CANCELLED,
            ]:
                instance.status = BookingStatus.CANCELLED
                instance.save()
            else:
                raise drf_permissions.PermissionDenied(
                    f"Невозможно отменить запись, которая уже '{instance.get_status_display()}' или завершена."
                )
        else:
            raise drf_permissions.PermissionDenied(
                "У вас нет прав для удаления этой записи."
            )
