# Используем официальный образ Python
FROM python:3.10-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Установка рабочего каталога
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock /app/

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

# Копируем остальной проект
COPY . /app/

# Команда для запуска Gunicorn
CMD ["gunicorn", "fitness_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
