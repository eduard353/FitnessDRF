from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    Используется для чтения и отображения данных пользователя,
    включая читаемые названия ролей и полов.
    """

    role_display = serializers.CharField(source="get_role_display", read_only=True)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "birthday",
            "gender",
            "gender_display",
            "phone_number",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["is_staff", "is_active", "date_joined", "last_login"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового пользователя.
    Требует пароль для записи и автоматически хеширует его.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "birthday",
            "gender",
            "phone_number",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "birthday",
            "gender",
            "phone_number",
            "role",
        ]
        read_only_fields = ["username"]
