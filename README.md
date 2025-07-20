# FitnessDRF

**FitnessDRF** — это API-сервис на Django REST Framework для управления расписаниями тренировок в фитнес-клубах.  
Система поддерживает три роли пользователей: **администратор**, **тренер** и **клиент**, каждая из которых имеет собственные права доступа.

---

## ⚙️ Функциональность

- Аутентификация через JWT
- Управление фитнес-клубами и профилями тренеров
- CRUD расписаний и бронирований
- Ролевая модель доступа (админ / тренер / клиент)
- Документация через Swagger/OpenAPI (`drf-spectacular`)

---

## 🧰 Технологии

- Python 3.10
- Django + Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- Poetry
- drf-spectacular (автогенерация документации)
- JWT (djangorestframework-simplejwt)

---

## 🚀 Быстрый старт (Docker)

### 1. Клонируйте проект:

```bash
git clone git@github.com:eduard353/FitnessDRF.git
cd FitnessDRF
```

### 2. Создайте `.env` файл:

```env
DEBUG=False
SECRET_KEY="your_key"
ALLOWED_HOSTS=127.0.0.1,localhost, your_domen

POSTGRES_DB=fitness_db_name
POSTGRES_USER=fitness_user_name
POSTGRES_PASSWORD=fitness_user_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

### 4. Примените миграции, соберите статику, создайте суперпользователя:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

### 5. Откройте в браузере:

- Главная: http://localhost/
- Админка: http://localhost/admin/
- Swagger UI: http://localhost/api/schema/swagger-ui/
---

## 📦 Структура контейнеров:

- `web` — Django-приложение с Gunicorn
- `db` — PostgreSQL 15
- `nginx` — отдача статики + прокси

---

## 🧪 Локальная разработка (Poetry)

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

---

## 🔒 Авторизация

- JWT токены через `djangorestframework-simplejwt`
- Получение токена:

```
POST /api/token/
{
  "username": "user",
  "password": "pass"
}
```

---

## 📂 Структура проекта

```
fitness_drf_back/
├── bookings/              # Приложение: Бронирования
├── fitness_backend/       # Основная Django-конфигурация (settings, wsgi и т.д.)
├── media/                 # Медиафайлы (загружаемые пользователями)
├── nginx/                 # Конфигурация Nginx (default.conf и пр.)
├── schedule/              # Приложение: Расписания тренировок
├── static/                # Статические файлы (после collectstatic)
├── trainers/              # Приложение: Тренеры
├── users/                 # Приложение: Пользователи и роли
├── Dockerfile             # Docker-инструкция для сборки контейнера
├── docker-compose.yml     # Docker Compose конфигурация
└── pyproject.toml         # Зависимости проекта (Poetry)
```

---
