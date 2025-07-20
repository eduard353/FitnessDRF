from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "client",
        "schedule_info",
        "booking_date",
        "booking_time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "booking_date",
        "schedule__trainer__user__last_name",
        "client__username",
    )
    search_fields = (
        "client__username",
        "client__first_name",
        "client__last_name",
        "schedule__trainer__user__first_name",
        "schedule__trainer__user__last_name",
    )
    readonly_fields = ("created_at", "updated_at")

    def schedule_info(self, obj):
        return (
            f"{obj.schedule.trainer.full_name} ({obj.schedule.start_time.strftime('%H:%M')}-"
            f"{obj.schedule.end_time.strftime('%H:%M')})"
        )

    schedule_info.short_description = "Расписание"
