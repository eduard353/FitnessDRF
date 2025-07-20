from django.db import models
from users.models import User, Role
from schedule.models import Schedule, DayOfWeek
from django.core.exceptions import ValidationError
from django.utils import timezone


class BookingStatus(models.TextChoices):
    PENDING = "pending", "Ожидает подтверждения"
    CONFIRMED = "confirmed", "Подтверждено"
    CANCELLED = "cancelled", "Отменено"
    COMPLETED = "completed", "Завершено"


class Booking(models.Model):
    """
    Модель для записи клиентов на тренировки.
    """

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.CLIENT},
        related_name="bookings",
        verbose_name="Клиент",
        help_text="Клиент, который осуществляет запись.",
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Расписание",
        help_text="Слот расписания, на который производится запись.",
    )
    booking_date = models.DateField(
        verbose_name="Дата записи",
        help_text="Конкретная дата, на которую производится запись.",
    )
    booking_time = models.TimeField(
        verbose_name="Время записи",
        help_text="Конкретное время, на которое производится запись. Должно совпадать со временем расписания.",
    )
    status = models.CharField(
        max_length=15,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name="Статус записи",
        help_text="Текущий статус записи (ожидает, подтверждено, отменено и т.д.).",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления записи"
    )

    class Meta:
        verbose_name = "Запись на тренировку"
        verbose_name_plural = "Записи на тренировки"
        unique_together = ("client", "schedule", "booking_date", "booking_time")
        ordering = ["-booking_date", "-booking_time"]
        indexes = [
            models.Index(fields=["client", "booking_date"]),
            models.Index(fields=["schedule", "booking_date", "booking_time"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return (
            f"Запись {self.client.username} на {self.schedule.trainer.full_name} "
            f"({self.booking_date} {self.booking_time.strftime('%H:%M')}) - "
            f"Статус: {self.get_status_display()}"
        )

    def clean(self):
        super().clean()

        if self.client and self.client.role != Role.CLIENT:
            raise ValidationError(
                {
                    "client": "Записываться на тренировку может только пользователь с ролью клиента."
                },
                code="not_a_client",
            )

        if self.booking_date < timezone.now().date():
            raise ValidationError(
                {"booking_date": "Нельзя записаться на прошедшую дату."},
                code="past_date",
            )

        day_of_week_int = list(DayOfWeek.values).index(self.schedule.day_of_week)
        if self.booking_date.weekday() != day_of_week_int:
            raise ValidationError(
                {
                    "booking_date": f'Дата записи ({self.booking_date.strftime("%A")}) не соответствует дню недели '
                    f"расписания"
                    f"({self.schedule.get_day_of_week_display()})."
                },
                code="day_mismatch",
            )

        if not (self.schedule.start_time <= self.booking_time < self.schedule.end_time):
            raise ValidationError(
                {
                    "booking_time": f'Время записи ({self.booking_time.strftime("%H:%M")}) должно находиться в пределах '
                    f"времени расписания"
                    f'({self.schedule.start_time.strftime("%H:%M")}-'
                    f'{self.schedule.end_time.strftime("%H:%M")}).'
                },
                code="time_mismatch",
            )

        if (
            Booking.objects.filter(
                schedule=self.schedule,
                booking_date=self.booking_date,
                booking_time=self.booking_time,
                status=BookingStatus.CONFIRMED,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"schedule": "Этот слот расписания уже занят другой записью."},
                code="slot_already_taken",
            )
