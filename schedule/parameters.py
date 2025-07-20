from drf_spectacular.utils import OpenApiParameter

trainer_id_param = OpenApiParameter(
    name="trainer_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Фильтрация расписаний по ID тренера.",
)

fitness_club_id_param = OpenApiParameter(
    name="fitness_club_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="Фильтрация расписаний по ID фитнес-клуба.",
)

date_param = OpenApiParameter(
    name="date",
    type=str,
    location=OpenApiParameter.QUERY,
    description=(
        "Фильтрация расписаний по дню недели, соответствующему указанной дате (формат: ГГГГ-ММ-ДД). "
        "Например, если 2025-07-17 был четверг, будут показаны все расписания, запланированные на четверг."
    ),
)
