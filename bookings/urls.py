from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet

router = DefaultRouter()
router.register(r"bookings", BookingViewSet)  # Маршруты для записей на тренировки

urlpatterns = [
    path("", include(router.urls)),
]
