from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitListAPIView(ListAPIView):
    """Вывод списка привычек авторизованного пользователя"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class HabitPublishedListAPIView(ListAPIView):
    """Вывод опубликованных привычек для всех пользователей"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitRetrieveAPIView(RetrieveAPIView):
    """Просмотр одной сущности(привычки)"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(UpdateAPIView):
    """Редактирование привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
