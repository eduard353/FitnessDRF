from drf_spectacular.utils import OpenApiParameter

schedule_id_param = OpenApiParameter(
    name="schedule_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Фильтрация по ID расписания.",
)

booking_date_param = OpenApiParameter(
    name="booking_date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Фильтрация по дате записи (формат: ГГГГ-ММ-ДД).",
)

status_param = OpenApiParameter(
    name="status",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Фильтрация по статусу записи (например, 'pending', 'confirmed', 'cancelled').",
)
