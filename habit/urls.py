from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitPublishedListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
)

app_name = HabitConfig.name

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="list"),
    path("published/", HabitPublishedListAPIView.as_view(), name="published"),
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="update"),
    path("retrieve/<int:pk>/", HabitRetrieveAPIView.as_view(), name="retrieve"),
    path("destroy/<int:pk>/", HabitDestroyAPIView.as_view(), name="destroy"),
]
