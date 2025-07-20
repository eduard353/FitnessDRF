from django.core.exceptions import ValidationError
from rest_framework import serializers

from schedule.models import Schedule
from users.models import User, Role
from .models import Booking
from users.serializers import UserSerializer
from schedule.serializers import ScheduleSerializer


class BookingSerializer(serializers.ModelSerializer):

    client = UserSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="client"),
        source="client",
        write_only=True,
        required=True,
    )
    schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(),
        source="schedule",
        write_only=True,
        required=True,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "client",
            "client_id",
            "schedule",
            "schedule_id",
            "booking_date",
            "booking_time",
            "status",
            "status_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        if "client" in data and "schedule" in data:
            client = data["client"]
            if client.role != Role.CLIENT:
                raise serializers.ValidationError(
                    {"client_id": "Пользователь должен иметь роль 'клиент'."}
                )

            instance = Booking(**data)
            try:
                instance.clean()
            except ValidationError as e:
                raise serializers.ValidationError(e.message_dict)

        return data
