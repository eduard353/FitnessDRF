from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "trainer",
        "fitness_club",
        "day_of_week",
        "start_time",
        "end_time",
        "is_active",
        "created_at",
    )
    list_filter = (
        "day_of_week",
        "is_active",
        "fitness_club",
        "trainer__user__last_name",
    )
    search_fields = (
        "trainer__user__first_name",
        "trainer__user__last_name",
        "fitness_club__name",
    )
    readonly_fields = ("created_at", "updated_at")
