from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FitnessClubViewSet, TrainerViewSet

router = DefaultRouter()
router.register(r"clubs", FitnessClubViewSet)
router.register(r"trainers", TrainerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
