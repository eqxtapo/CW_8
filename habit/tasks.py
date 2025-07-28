from datetime import datetime, timedelta

from celery import shared_task

from habit.models import Habit
from habit.services import send_telegram_message


@shared_task
def send_reminder():
    """Отправляет напоминание пользователю,
    о том, что нужно выполнить привычку в назначенное время"""

    current_time = datetime.now()
    current_time_less = current_time - timedelta(seconds=30)

    for habit in Habit.objects.filter(
        time__lte=current_time.time(), time__gte=current_time_less.time()
    ):
        if habit.user.tg_chat_id:
            chat_id = habit.user.tg_chat_id
            message = f"Я буду {habit.action} в {habit.time} в {habit.place}"
            send_telegram_message(chat_id, message)
            print("Уведомление отправлено")
