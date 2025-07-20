from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view

from users.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer

common_tags = {"users": ["Аутентификация и Пользователи"]}

create_user_extend_schema = extend_schema(
    summary="Регистрация нового клиента",
    description="""
    Регистрирует нового пользователя с ролью `client` по умолчанию.
    Доступ открыт для всех, **авторизация не требуется**.

    После успешной регистрации (HTTP 201 Created) необходимо выполнить запрос к конечной точке `/api/token/` 
    для получения JWT-токенов (access и refresh), которые будут использоваться для последующих авторизованных 
    запросов к API.
    """,
    request=UserCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer, description="Пользователь успешно зарегистрирован."
        ),
        400: OpenApiResponse(
            description=(
                "Неверные данные запроса. "
                "Например: логин или email уже заняты, пароль не соответствует требованиям "
                "(слишком короткий, простой и т.д.), или другие ошибки валидации."
            )
        ),
    },
    tags=common_tags["users"],
    auth=[],
)


me_extend_schema_view = extend_schema_view(
    get=extend_schema(
        summary="Получение собственного профиля",
        description="Позволяет аутентифицированному пользователю просмотреть детальную информацию о своем профиле.",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(
                description="Неавторизованный доступ. Не предоставлен токен авторизации или он недействителен."
            ),
        },
        tags=["Аутентификация и Пользователи"],
    ),
    put=extend_schema(
        summary="Полное обновление собственного профиля",
        description=(
            "Позволяет аутентифицированному пользователю полностью обновить данные своего профиля. "
            "Требует передачи всех полей профиля."
        ),
        request=UserUpdateSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(
                description="Неверные данные запроса. Ошибки валидации."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description=(
                    "Доступ запрещен (хотя в данном случае, если пользователь авторизован, "
                    "эта ошибка маловероятна)."
                )
            ),
        },
        tags=["Аутентификация и Пользователи"],
    ),
    patch=extend_schema(
        summary="Частичное обновление собственного профиля",
        description=(
            "Позволяет аутентифицированному пользователю частично обновить данные своего профиля. "
            "Можно передать одно или несколько изменяемых полей."
        ),
        request=UserUpdateSerializer(partial=True),
        responses={
            200: UserSerializer,
            400: OpenApiResponse(
                description="Неверные данные запроса. Ошибки валидации."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещен."),
        },
        tags=["Аутентификация и Пользователи"],
    ),
    delete=extend_schema(
        summary="Удаление собственного аккаунта",
        description=(
            "Позволяет аутентифицированному пользователю удалить свой аккаунт из системы. "
            "**Внимание: это действие необратимо!**"
        ),
        responses={
            204: OpenApiResponse(
                description="Аккаунт успешно удален. Тело ответа отсутствует."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещен."),
        },
        tags=["Аутентификация и Пользователи"],
    ),
)


user_admin_extend_schema_view = extend_schema_view(
    list=extend_schema(
        summary="Список всех пользователей",
        description="Получение списка всех зарегистрированных пользователей системы. Доступно только администраторам.",
        tags=["Пользователи (Админ)"],
        responses={
            200: UserSerializer(many=True),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Доступ запрещён (доступно только администраторам)."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Получить пользователя по ID",
        description="Получение детальной информации о пользователе по его ID. Доступно только администраторам.",
        tags=["Пользователи (Админ)"],
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Пользователь не найден."),
        },
    ),
    create=extend_schema(
        summary="Создать нового пользователя",
        description=(
            "Создание нового пользователя в системе. Доступно только администраторам. "
            "Пароль будет автоматически хэширован."
        ),
        tags=["Пользователи (Админ)"],
        request=UserCreateSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(
                description="Неверные данные запроса (например, невалидный email, слишком короткий пароль)."
            ),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
        },
    ),
    update=extend_schema(
        summary="Обновить пользователя (полностью)",
        description=(
            "Полное обновление информации о существующем пользователе по его ID. "
            "Доступно только администраторам. Требует передачи всех полей."
        ),
        tags=["Пользователи (Админ)"],
        request=UserUpdateSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Пользователь не найден."),
        },
    ),
    partial_update=extend_schema(
        summary="Частично обновить пользователя",
        description=(
            "Частичное обновление информации о существующем пользователе по его ID. "
            "Доступно только администраторам. Позволяет обновлять одно или несколько полей."
        ),
        tags=["Пользователи (Админ)"],
        request=UserUpdateSerializer(partial=True),
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Неверные данные запроса."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Пользователь не найден."),
        },
    ),
    destroy=extend_schema(
        summary="Удалить пользователя",
        description="Удаление пользователя из системы по его ID. Доступно только администраторам.",
        tags=["Пользователи (Админ)"],
        responses={
            204: OpenApiResponse(description="Пользователь успешно удален."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(description="Доступ запрещён."),
            404: OpenApiResponse(description="Пользователь не найден."),
        },
    ),
)
