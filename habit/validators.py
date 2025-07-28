from rest_framework.exceptions import ValidationError

from habit.models import Habit


class AssociatedWithoutRewardValidator:
    """
    Исключаем одновременный выбор связанной привычки и указания вознаграждения.
    """

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, habit):
        if habit.get("associted_habit") and habit.get("reward"):
            raise ValidationError(
                "В модели не должно быть заполнено одновременно и поле вознаграждения,"
                "и поле связанной привычки. Можно заполнить только одно из двух полей."
            )


class LeadTimeValidator:
    """
    Время выполнения должно быть не больше 120 секунд.
    """

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, habit):
        if habit.get("time_to_complete"):
            habit_time = habit.get("time_to_complete")
            if habit_time > 120:
                raise ValidationError(
                    "Время выполнения должно быть не больше 120 секунд."
                )


class NiceHabitInAssociatedValidator:
    """
    В связанные привычки могут попадать только привычки с признаком приятной привычки.
    """

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, habit):

        if habit.get("associted_habit"):
            associted_habit = Habit.objects.get(pk=habit.get("associted_habit").pk)
            if not associted_habit.nice_habit:
                raise ValidationError(
                    "В связанные привычки могут попадать только привычки с признаком приятной привычки."
                )


class NiceHabitWithoutValidator:
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, habit):
        if habit.get("nice_habit"):
            if habit.get("reward") or habit.get("associted_habit"):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, habit):
        if habit.get("periodicity"):
            periodicity = habit.get("periodicity")
            if 7 < periodicity:
                raise ValidationError(
                    "За одну неделю необходимо выполнить привычку хотя бы один раз."
                )
