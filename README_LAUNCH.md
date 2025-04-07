# Инструкция по запуску проекта "Социальная сеть для обмена фотографиями"

## Требования:
- Python 3.x
- PostgreSQL
- Git

## Установка и запуск:

1. Клонировать репозиторий:
```
git clone <ссылка на репозиторий>
cd spd-diplom
```

2. Создать и активировать виртуальное окружение:
```
python -m venv .venv
.venv\Scripts\activate  # для Windows
source .venv/bin/activate  # для Linux/Mac
```

3. Установить зависимости:
```
pip install django djangorestframework psycopg2 pillow django-environ
```

4. Создать файл .env в корне проекта и добавить настройки базы данных:
```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/social_network_db
```
Примечание: замените postgres:postgres на ваш логин:пароль от PostgreSQL

5. Создать базу данных PostgreSQL:
```
psql -U postgres -c "CREATE DATABASE social_network_db;"
```

6. Выполнить миграции:
```
python manage.py migrate
```

7. Создать суперпользователя для доступа к админке:
```
python manage.py createsuperuser
```

8. Запустить сервер разработки:
```
python manage.py runserver
```

## Интерфейс проекта:

- Админ-панель: http://127.0.0.1:8000/admin/
- API Endpoints:
  - Список постов: http://127.0.0.1:8000/api/posts/
  - Детали поста: http://127.0.0.1:8000/api/posts/<id>/
  - Добавить комментарий: http://127.0.0.1:8000/api/posts/<id>/add_comment/
  - Поставить/убрать лайк: http://127.0.0.1:8000/api/posts/<id>/like/

## Функциональность:

- **Создание постов**: авторизованные пользователи могут создавать посты с текстом и изображением
- **Редактирование постов**: только автор может редактировать свой пост
- **Комментирование**: авторизованные пользователи могут оставлять комментарии к постам
- **Лайки**: авторизованные пользователи могут ставить и убирать лайки к постам 