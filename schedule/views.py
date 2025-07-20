from rest_framework import viewsets, permissions as drf_permissions

from trainers.models import Trainer
from users.models import Role
from .models import Schedule
from .schemas import schedule_extend_schema_view
from .serializers import ScheduleSerializer
from . import permissions as local_permissions
from datetime import datetime
from rest_framework.exceptions import ValidationError


@schedule_extend_schema_view
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by("day_of_week", "start_time")
    serializer_class = ScheduleSerializer
    permission_classes = [local_permissions.IsAdminOrTrainerOwnerOfSchedule]

    def get_queryset(self):
        queryset = super().get_queryset()

        trainer_id = self.request.query_params.get("trainer_id")
        if trainer_id:
            queryset = queryset.filter(trainer__id=trainer_id)

        fitness_club_id = self.request.query_params.get("fitness_club_id")
        if fitness_club_id:
            queryset = queryset.filter(fitness_club__id=fitness_club_id)

        date_param = self.request.query_params.get("date")
        if date_param:
            try:
                target_date = datetime.strptime(date_param, "%Y-%m-%d").date()
                # Соответствие дня недели из расписания (0=понедельник, 6=воскресенье)
                day_of_week_map = {
                    0: "monday",
                    1: "tuesday",
                    2: "wednesday",
                    3: "thursday",
                    4: "friday",
                    5: "saturday",
                    6: "sunday",
                }
                day_name = day_of_week_map.get(target_date.weekday())
                if day_name:
                    queryset = queryset.filter(day_of_week=day_name)
                else:
                    return queryset.none()
            except ValueError:
                raise ValidationError(
                    {"date": "Неверный формат даты. Используйте YYYY-MM-DD."}
                )

        if (
            self.request.user.is_authenticated
            and self.request.user.role == Role.TRAINER
            and not self.request.user.is_staff
        ):
            try:
                trainer_profile = Trainer.objects.get(user=self.request.user)
                queryset = queryset.filter(trainer=trainer_profile)
            except Trainer.DoesNotExist:
                return queryset.none()

        return queryset

    def perform_create(self, serializer):
        if self.request.user.role == Role.TRAINER and not self.request.user.is_staff:
            try:
                trainer_profile = Trainer.objects.get(user=self.request.user)
                if (
                    "trainer" in serializer.validated_data
                    and serializer.validated_data["trainer"] != trainer_profile
                ):
                    raise drf_permissions.PermissionDenied(
                        "Вы можете создавать расписание только для себя."
                    )
                serializer.save(trainer=trainer_profile)
            except Trainer.DoesNotExist:
                raise drf_permissions.PermissionDenied(
                    "Вы не можете создать расписание, так как у вас нет профиля тренера."
                )
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user.role == Role.TRAINER and not self.request.user.is_staff:
            try:
                trainer_profile = Trainer.objects.get(user=self.request.user)
                if serializer.instance.trainer != trainer_profile:
                    raise drf_permissions.PermissionDenied(
                        "Вы можете обновлять только свое расписание."
                    )
                serializer.save()
            except Trainer.DoesNotExist:
                raise drf_permissions.PermissionDenied(
                    "Ошибка: у вас нет профиля тренера."
                )
        else:
            serializer.save()
