from rest_framework import serializers

from trainers.models import Trainer, FitnessClub
from .models import Schedule
from trainers.serializers import TrainerSerializer, FitnessClubSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(read_only=True)
    fitness_club = FitnessClubSerializer(read_only=True)
    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display", read_only=True
    )
    trainer_id = serializers.PrimaryKeyRelatedField(
        queryset=Trainer.objects.all(), source="trainer", write_only=True, required=True
    )
    fitness_club_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClub.objects.all(),
        source="fitness_club",
        write_only=True,
        required=True,
    )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "trainer",
            "trainer_id",
            "fitness_club",
            "fitness_club_id",
            "day_of_week",
            "day_of_week_display",
            "start_time",
            "end_time",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
