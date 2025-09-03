FROM python:3.11-slim-bullseye

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Порт для приложения
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]

