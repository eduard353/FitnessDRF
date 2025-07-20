from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from trainers.serializers import FitnessClubSerializer, TrainerSerializer


common_tags = {"fitnessclub": ["Фитнес-клубы"], "trainer": ["Тренеры"]}

fitnessclub_extend_schema_view = extend_schema_view(
    list=extend_schema(
        summary="Список фитнес-клубов",
        description="Получение списка всех зарегистрированных фитнес-клубов. Доступно всем пользователям.",
        tags=common_tags["fitnessclub"],
        responses={
            200: FitnessClubSerializer(many=True),
            401: OpenApiResponse(description="Неавторизованный доступ."),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о фитнес-клубе",
        description="Получение детальной информации о конкретном фитнес-клубе по его ID. Доступно всем пользователям.",
        tags=common_tags["fitnessclub"],
        responses={
            200: FitnessClubSerializer,
            401: OpenApiResponse(description="Неавторизованный доступ."),
            404: OpenApiResponse(description="Фитнес-клуб не найден."),
        },
    ),
    create=extend_schema(
        summary="Создание фитнес-клуба (только админ)",
        description="Создание нового фитнес-клуба. Доступно только администраторам.",
        tags=common_tags["fitnessclub"],
        request=FitnessClubSerializer,
        responses={
            201: FitnessClubSerializer,
            400: OpenApiResponse(
                description="Неверные данные запроса. Ошибки валидации."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Доступ запрещён (доступно только администраторам)."
            ),
        },
    ),
    update=extend_schema(
        summary="Полное обновление фитнес-клуба (только админ)",
        description=(
            "Полное обновление информации о существующем фитнес-клубе по его ID. "
            "Доступно только администраторам. Требует передачи всех полей."
        ),
        tags=common_tags["fitnessclub"],
        request=FitnessClubSerializer,
        responses={
            200: FitnessClubSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Фитнес-клуб не найден."),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление фитнес-клуба (только админ)",
        description=(
            "Частичное обновление информации о существующем фитнес-клубе по его ID. "
            "Доступно только администраторам. Позволяет обновлять одно или несколько полей."
        ),
        tags=common_tags["fitnessclub"],
        request=FitnessClubSerializer(partial=True),
        responses={
            200: FitnessClubSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Фитнес-клуб не найден."),
        },
    ),
    destroy=extend_schema(
        summary="Удаление фитнес-клуба (только админ)",
        description="Удаление фитнес-клуба из системы по его ID. Доступно только администраторам.",
        tags=common_tags["fitnessclub"],
        responses={
            204: OpenApiResponse(
                description="Фитнес-клуб успешно удален. Тело ответа отсутствует."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Фитнес-клуб не найден."),
        },
    ),
)


trainer_extend_schema_view = extend_schema_view(
    list=extend_schema(
        summary="Список тренеров",
        description="Получение списка всех профилей тренеров. Доступно всем аутентифицированным пользователям.",
        responses={
            200: TrainerSerializer(many=True),
            401: OpenApiResponse(description="Неавторизованный доступ."),
        },
        tags=common_tags["trainer"],
    ),
    retrieve=extend_schema(
        summary="Получить профиль тренера",
        description=(
            "Получение детальной информации о профиле тренера по его ID. "
            "Доступно всем аутентифицированным пользователям."
        ),
        responses={
            200: TrainerSerializer,
            401: OpenApiResponse(description="Неавторизованный доступ."),
            404: OpenApiResponse(description="Профиль тренера не найден."),
        },
        tags=common_tags["trainer"],
    ),
    create=extend_schema(
        summary="Создание профиля тренера",
        description=(
            "Создание нового профиля тренера. Доступно администраторам и пользователям с ролью 'тренер'. "
            "Тренер может создать профиль только для себя, если у него его еще нет. "
            "Администратор может создать профиль для любого пользователя."
        ),
        request=TrainerSerializer,
        responses={
            201: TrainerSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Доступ запрещён (у пользователя уже есть профиль тренера или неподходящая роль)."
            ),
        },
        tags=common_tags["trainer"],
    ),
    update=extend_schema(
        summary="Полное обновление профиля тренера",
        description=(
            "Полное обновление информации о профиле тренера. "
            "Доступно администраторам и владельцу профиля тренера."
        ),
        request=TrainerSerializer,
        responses={
            200: TrainerSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Профиль тренера не найден."),
        },
        tags=common_tags["trainer"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление профиля тренера",
        description=(
            "Частичное обновление информации о профиле тренера. "
            "Доступно администраторам и владельцу профиля тренера."
        ),
        request=TrainerSerializer(partial=True),
        responses={
            200: TrainerSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Профиль тренера не найден."),
        },
        tags=common_tags["trainer"],
    ),
    destroy=extend_schema(
        summary="Удаление профиля тренера",
        description="Удаление существующего профиля тренера. Доступно только администраторам.",
        responses={
            204: OpenApiResponse(description="Профиль тренера успешно удален."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Доступ запрещён (доступно только администраторам)."
            ),
            404: OpenApiResponse(description="Профиль тренера не найден."),
        },
        tags=common_tags["trainer"],
    ),
)
