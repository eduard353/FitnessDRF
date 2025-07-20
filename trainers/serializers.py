from rest_framework import serializers

from users.models import User
from .models import Trainer, FitnessClub
from users.serializers import UserSerializer


class FitnessClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClub
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class TrainerSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    clubs = FitnessClubSerializer(many=True, read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="trainer"),
        source="user",
        write_only=True,
        required=True,
        help_text="ID пользователя с ролью 'тренер', связанного с этим профилем тренера.",
    )

    class Meta:
        model = Trainer
        fields = [
            "id",
            "user",
            "user_id",
            "description",
            "specialization",
            "experience_years",
            "clubs",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
