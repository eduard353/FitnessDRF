from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import User, Role
from .schemas import (
    create_user_extend_schema,
    me_extend_schema_view,
    user_admin_extend_schema_view,
)
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer


@create_user_extend_schema
class RegisterView(generics.CreateAPIView):
    """
    Представление для регистрации нового пользователя.
    Доступно всем. Создает пользователя с ролью 'client' по умолчанию.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        serializer.save(role=Role.CLIENT)


@me_extend_schema_view
class MeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления информации о текущем аутентифицированном пользователе.
    Доступно только аутентифицированным пользователям.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Метод для получения объекта, с которым будет работать View.
        Возвращает текущего аутентифицированного пользователя.
        """
        return self.request.user

    def get_serializer_class(self):
        """
        Возвращает подходящий сериализатор в зависимости от действия.
        Для обновления (PUT/PATCH) используем UserUpdateSerializer.
        Для получения (GET) и удаления (DELETE) используем UserSerializer.
        """
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        """
        Выполняет удаление пользователя.
        """
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@user_admin_extend_schema_view
class UserAdminViewSet(viewsets.ModelViewSet):
    """
    Представление для управления всеми пользователями (CRUD) администратором.
    Доступно только администраторам.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer
