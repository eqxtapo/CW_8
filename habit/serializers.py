from rest_framework.serializers import ModelSerializer

from habit.models import Habit
from habit.validators import (
    AssociatedWithoutRewardValidator,
    LeadTimeValidator,
    NiceHabitInAssociatedValidator,
    NiceHabitWithoutValidator,
    PeriodicityValidator,
)


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            AssociatedWithoutRewardValidator(
                field1="associated_habit", field2="reward"
            ),
            LeadTimeValidator(field1="time_to_complete"),
            NiceHabitInAssociatedValidator(field1="associated_habit"),
            NiceHabitWithoutValidator(
                field1="nice_habit", field2="reward", field3="associated_habit"
            ),
            PeriodicityValidator(field1="periodicity"),
        ]
