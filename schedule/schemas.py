from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from .serializers import ScheduleSerializer
from .parameters import trainer_id_param, fitness_club_id_param, date_param

common_tags = {"schedule": ["Расписания"]}


schedule_extend_schema_view = extend_schema_view(
    list=extend_schema(
        summary="Список расписаний",
        description=(
            "Получение списка всех расписаний тренировок. "
            "Клиенты и гости видят все расписания. "
            "Тренеры видят только свои расписания. "
            "Поддерживается фильтрация по ID тренера, ID фитнес-клуба и дате."
        ),
        parameters=[trainer_id_param, fitness_club_id_param, date_param],
        responses={
            200: ScheduleSerializer(many=True),
            400: OpenApiResponse(description="Неверный формат даты."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
        },
        tags=common_tags["schedule"],
    ),
    retrieve=extend_schema(
        summary="Детали расписания",
        description=(
            "Получение детальной информации о конкретном расписании по его ID. "
            "Доступно всем аутентифицированным пользователям."
        ),
        responses={
            200: ScheduleSerializer,
            401: OpenApiResponse(description="Неавторизованный доступ."),
            404: OpenApiResponse(description="Расписание не найдено."),
        },
        tags=common_tags["schedule"],
    ),
    create=extend_schema(
        summary="Создание расписания",
        description=(
            "Создание нового расписания. Доступно администраторам и тренерам. "
            "Тренеры могут создавать расписания только для себя (автоматически привязываются)."
        ),
        request=ScheduleSerializer,
        responses={
            201: ScheduleSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Доступ запрещён (например, тренер пытается создать расписание для другого тренера)."
            ),
        },
        tags=common_tags["schedule"],
    ),
    update=extend_schema(
        summary="Полное обновление расписания",
        description=(
            "Полное обновление информации о расписании. Доступно администраторам и тренерам. "
            "Тренеры могут обновлять только свои расписания."
        ),
        request=ScheduleSerializer,
        responses={
            200: ScheduleSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Расписание не найдено."),
        },
        tags=common_tags["schedule"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление расписания",
        description=(
            "Частичное обновление информации о расписании. Доступно администраторам и тренерам. "
            "Тренеры могут обновлять только свои расписания."
        ),
        request=ScheduleSerializer(partial=True),
        responses={
            200: ScheduleSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Расписание не найдено."),
        },
        tags=common_tags["schedule"],
    ),
    destroy=extend_schema(
        summary="Удаление расписания",
        description="Удаление существующего расписания. Доступно только администраторам.",
        responses={
            204: OpenApiResponse(description="Расписание успешно удалено."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Расписание не найдено."),
        },
        tags=common_tags["schedule"],
    ),
)
