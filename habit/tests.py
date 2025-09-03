from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестировка CRUD привычек"""

    def setUp(self):
        self.user = User.objects.create(email="test@mail.com")
        self.habit = Habit.objects.create(
            action="прогулка с собакой в 7 утра", user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        """Детальный просмотр"""
        url = reverse("habit:retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "прогулка с собакой в 7 утра")

    def test_habit_create(self):
        """Создание"""
        url = reverse("habit:create")
        data = {"action": "пробежка в парке"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("user"), self.user.pk)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Детальный просмотр"""
        url = reverse("habit:update", args=(self.habit.pk,))
        data = {"action": "прогулка с собакой в 7 утра"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("action"), "прогулка с собакой в 7 утра")

        data = {"periodicity": 8}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("non_field_errors"),
            ["За одну неделю необходимо выполнить привычку хотя бы один раз."],
        )

    def test_habit_delete(self):
        """Удаление"""
        url = reverse("habit:destroy", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_list(self):
        """Список привычек"""
        url = reverse("habit:list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": None,
                    "time": None,
                    "action": "прогулка с собакой в 7 утра",
                    "nice_habit": False,
                    "periodicity": 1,
                    "reward": None,
                    "is_published": True,
                    "time_to_complete": None,
                    "user": self.user.pk,
                    "associted_habit": None,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_list_published(self):
        """Список опубликованных привычек"""
        url = reverse("habit:published")

        response = self.client.get(url)
        data = response.json()
        print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": None,
                    "time": None,
                    "action": "прогулка с собакой в 7 утра",
                    "nice_habit": False,
                    "periodicity": 1,
                    "reward": None,
                    "is_published": True,
                    "time_to_complete": None,
                    "user": self.user.pk,
                    "associted_habit": None,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
