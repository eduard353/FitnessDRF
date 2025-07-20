from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from .serializers import BookingSerializer
from .parameters import schedule_id_param, booking_date_param, status_param

common_tags = {"booking": ["Записи"]}


booking_extend_schema_view = extend_schema_view(
    list=extend_schema(
        summary="Список записей",
        description=(
            "Получение списка всех записей на тренировки. Администраторы видят все записи. "
            "Тренеры видят записи на тренировки из их расписаний. Клиенты видят только свои записи. "
            "Поддерживается фильтрация по ID расписания, дате записи и статусу."
        ),
        parameters=[schedule_id_param, booking_date_param, status_param],
        responses={
            200: BookingSerializer(many=True),
            401: OpenApiResponse(description="Неавторизованный доступ."),
        },
        tags=common_tags["booking"],
    ),
    retrieve=extend_schema(
        summary="Получение записи",
        description="Получение детальной информации о конкретной записи по ее ID.",
        responses={
            200: BookingSerializer,
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Запись не найдена."),
        },
        tags=common_tags["booking"],
    ),
    create=extend_schema(
        summary="Создание записи на тренировку",
        description=(
            "Создание новой записи на тренировку. Клиент автоматически привязывается к создаваемой записи. "
            "Администраторы могут создавать записи для любого клиента, указывая его ID."
        ),
        request=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
        },
        tags=common_tags["booking"],
    ),
    update=extend_schema(
        summary="Полное обновление записи",
        description=(
            "Полное обновление записи. Клиенты могут только отменить свою запись. "
            "Администраторы могут редактировать любые поля."
        ),
        request=BookingSerializer,
        responses={
            200: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Запись не найдена."),
        },
        tags=common_tags["booking"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление записи",
        description="То же, что и полное, но позволяет обновлять только часть полей.",
        request=BookingSerializer(partial=True),
        responses={
            200: BookingSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Запись не найдена."),
        },
        tags=common_tags["booking"],
    ),
    destroy=extend_schema(
        summary="Удаление или отмена записи",
        description=(
            "Удаление записи администратором или отмена клиентом. "
            "Нельзя отменить завершенные или уже отменённые записи."
        ),
        responses={
            204: OpenApiResponse(description="Успешно."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Запись не найдена."),
        },
        tags=common_tags["booking"],
    ),
)
