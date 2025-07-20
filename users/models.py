from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


phone_regex = RegexValidator(
    regex=r"^(?:\+7|8)\d{10}$",
    message="Номер телефона должен начинаться с +7 или 8 и содержать 10 цифр.",
)


class Role(models.TextChoices):
    CLIENT = "client", "Клиент"
    TRAINER = "trainer", "Тренер"
    ADMIN = "admin", "Администратор"


class Gender(models.TextChoices):
    MALE = "M", "Мужской"
    FEMALE = "F", "Женский"


class User(AbstractUser):
    """
    Кастомная модель пользователя для фитнес-приложения.
    Расширяет стандартного пользователя Django дополнительными полями
    и управлением ролями.
    """

    email = models.EmailField("Email", unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Дата рождения пользователя.",
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        null=True,
        verbose_name="Пол",
        help_text="Пол пользователя.",
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=12,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Телефон",
        help_text="Контактный телефон пользователя.",
    )

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_client(self):
        return self.role == Role.CLIENT

    @property
    def is_trainer(self):
        return self.role == Role.TRAINER

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
