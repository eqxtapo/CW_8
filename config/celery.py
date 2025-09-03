from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра объекта Celery
app = Celery("config")

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

# Автоматическое обнаружение и регистрация задач из файлов tasks.py
app.autodiscover_tasks()
