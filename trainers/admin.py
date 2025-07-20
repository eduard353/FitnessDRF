from django.contrib import admin
from .models import Trainer, FitnessClub


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "full_name",
        "specialization",
        "experience_years",
        "display_clubs",
        "created_at",
    )
    list_filter = ("specialization", "experience_years", "clubs")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "description",
        "specialization",
    )
    readonly_fields = ("created_at", "updated_at")

    def display_clubs(self, obj):
        return ", ".join([club.name for club in obj.clubs.all()])

    display_clubs.short_description = "Клубы"


@admin.register(FitnessClub)
class FitnessClubAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone_number", "created_at")
    search_fields = ("name", "address", "phone_number")
    readonly_fields = ("created_at", "updated_at")
