# schedule/models.py
from django.db import models
from trainers.models import Trainer, FitnessClub
from django.core.exceptions import ValidationError
from datetime import (
    timedelta,
    datetime,
)  # Не нужны MinValueValidator, MaxValueValidator, time, т.к. max_clients удален


class DayOfWeek(models.TextChoices):
    MONDAY = "monday", "Понедельник"
    TUESDAY = "tuesday", "Вторник"
    WEDNESDAY = "wednesday", "Среда"
    THURSDAY = "thursday", "Четверг"
    FRIDAY = "friday", "Пятница"
    SATURDAY = "saturday", "Суббота"
    SUNDAY = "sunday", "Воскресенье"


# TrainingType класс удален, так как training_type больше не используется в Schedule


class Schedule(models.Model):
    """
    Модель для расписания тренировок тренеров.
    Теперь не различает индивидуальные/групповые тренировки и не отслеживает максимальное количество клиентов.
    """

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Тренер",
        help_text="Тренер, для которого создано это расписание.",
    )
    fitness_club = models.ForeignKey(
        FitnessClub,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Фитнес-клуб",
        help_text="Фитнес-клуб, в котором проходит тренировка.",
    )
    day_of_week = models.CharField(
        max_length=10,
        choices=DayOfWeek.choices,
        verbose_name="День недели",
        help_text="День недели, в который проводится тренировка.",
    )
    start_time = models.TimeField(
        verbose_name="Время начала", help_text="Время начала тренировки (ЧЧ:ММ)."
    )
    end_time = models.TimeField(
        verbose_name="Время окончания", help_text="Время окончания тренировки (ЧЧ:ММ)."
    )
    # Поля training_type и max_clients удалены

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
        help_text="Указывает, активно ли это расписание в данный момент.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания расписания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления расписания"
    )

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        # Уникальность расписания по тренеру, клубу, дню и времени начала/конца
        unique_together = (
            "trainer",
            "fitness_club",
            "day_of_week",
            "start_time",
            "end_time",
        )
        ordering = ["day_of_week", "start_time"]
        indexes = [  # Индексы сохраняем, так как они полезны для запросов
            models.Index(fields=["trainer", "day_of_week", "start_time"]),
            models.Index(fields=["fitness_club", "day_of_week"]),
        ]

    def __str__(self):
        return (
            f"Расписание {self.trainer.full_name} в {self.fitness_club.name} "
            f"({self.get_day_of_week_display()}, {self.start_time.strftime('%H:%M')}-"
            f"{self.end_time.strftime('%H:%M')})"
        )

    def clean(self):
        super().clean()

        # 1. Валидация времени начала и окончания
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    {"end_time": "Время окончания должно быть позже времени начала."}
                )

            dummy_date = (
                datetime.min.date()
            )  # Используем фиктивную дату для создания datetime объектов
            start_dt = datetime.combine(dummy_date, self.start_time)
            end_dt = datetime.combine(dummy_date, self.end_time)

            duration = end_dt - start_dt
            if duration < timedelta(minutes=15):
                raise ValidationError(
                    {
                        "start_time": "Длительность тренировки должна быть не менее 15 минут."
                    }
                )
            if duration > timedelta(hours=8):  # Максимальная длительность тренировки
                raise ValidationError(
                    {"end_time": "Длительность тренировки не должна превышать 8 часов."}
                )

        # 2. Валидация: тренер должен быть привязан к данному фитнес-клубу
        if self.trainer and self.fitness_club:
            if self.fitness_club not in self.trainer.clubs.all():
                raise ValidationError(
                    {
                        "fitness_club": "Выбранный тренер не работает в этом фитнес-клубе."
                    },
                    code="trainer_not_in_club",
                )
