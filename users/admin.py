from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from trainers.models import Trainer


class TrainerInline(admin.StackedInline):
    model = Trainer
    can_delete = False
    verbose_name_plural = "Тренерский профиль"
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (TrainerInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = ("is_staff", "is_active", "role", "gender")

    search_fields = ("username", "email", "first_name", "last_name", "phone_number")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "birthday",
                    "gender",
                    "phone_number",
                )
            },
        ),
        (
            "Разрешения",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                )
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("date_joined", "last_login")
