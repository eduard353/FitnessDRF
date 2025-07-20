from rest_framework import viewsets, permissions as drf_permissions
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Trainer, FitnessClub
from . import permissions as local_permissions
from .schemas import fitnessclub_extend_schema_view, trainer_extend_schema_view
from .serializers import TrainerSerializer, FitnessClubSerializer
from users.models import Role


@fitnessclub_extend_schema_view
class FitnessClubViewSet(viewsets.ModelViewSet):
    queryset = FitnessClub.objects.all().order_by("name")
    serializer_class = FitnessClubSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]


@trainer_extend_schema_view
class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all().order_by("user__last_name", "user__first_name")
    serializer_class = TrainerSerializer
    permission_classes = [local_permissions.IsAdminOrTrainerOwner]

    def perform_create(self, serializer):

        if not self.request.user.is_staff:
            if self.request.user.role != Role.TRAINER:
                raise drf_permissions.PermissionDenied(
                    "Вы не можете создать профиль тренера, ваша роль не 'тренер'."
                )
            if Trainer.objects.filter(user=self.request.user).exists():
                raise drf_permissions.PermissionDenied(
                    "У вас уже есть профиль тренера."
                )
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.role == Role.TRAINER
            and not self.request.user.is_staff
        ):
            # Тренер может просматривать всех, но для редактирования нужна has_object_permission
            return Trainer.objects.all().order_by("user__last_name")
        return super().get_queryset()
