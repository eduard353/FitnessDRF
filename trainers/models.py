from django.db import models
from users.models import User, Role
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError


club_phone_regex = RegexValidator(
    regex=r"^(?:\+7|8)\d{10}$",
    message="Номер телефона клуба должен начинаться с +7 или 8 и содержать 10 цифр.",
)


class FitnessClub(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название зала",
        help_text="Уникальное название фитнес-клуба.",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Адрес",
        help_text="Полный адрес фитнес-клуба.",
    )
    phone_number = models.CharField(
        validators=[club_phone_regex],
        max_length=12,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Контактный телефон фитнес-клуба.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Краткое описание фитнес-клуба.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Фитнес-клуб"
        verbose_name_plural = "Фитнес-клубы"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Trainer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": Role.TRAINER},
        related_name="trainer_profile",
        verbose_name="Пользователь",
        help_text="Привязанный пользователь с ролью 'тренер'.",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Подробное описание квалификации и опыта тренера.",
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Специализация",
        help_text="Основная специализация тренера (например, 'силовые тренировки', 'йога').",
    )
    experience_years = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Опыт (лет)",
        help_text="Количество лет опыта работы тренером.",
        validators=[
            MinValueValidator(0, message="Опыт не может быть отрицательным."),
            MaxValueValidator(60, message="Опыт не может превышать 60 лет."),
        ],
    )

    clubs = models.ManyToManyField(
        FitnessClub,
        related_name="trainers",
        verbose_name="Фитнес-клубы, в которых работает",
        help_text="Список фитнес-клубов, где работает тренер.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания профиля"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего обновления профиля"
    )

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def clean(self):
        super().clean()
        # Проверка: связанный пользователь должен иметь роль 'TRAINER'
        if self.user and self.user.role != Role.TRAINER:
            raise ValidationError(
                {
                    "user": 'Вы можете привязать к профилю тренера только пользователя с ролью "Тренер".'
                },
                code="invalid_user_role",
            )

        if self.user and self.user.birthday:
            today = date.today()
            age = (
                today.year
                - self.user.birthday.year
                - (
                    (today.month, today.day)
                    < (self.user.birthday.month, self.user.birthday.day)
                )
            )
            if age < 18:
                raise ValidationError(
                    {"user": "Тренер должен быть старше 18 лет."},
                    code="min_age_trainer",
                )
