# Сервис микроблогов на Flask

Учебный дипломный проект курса Python Advanced: серверная часть социальной сети с постами, лайками, подписками и загрузкой изображений. Backend подключён к готовой сборке frontend из задания; клиентская часть не заявляется как собственная разработка.

## Реализовано

- REST API для публикации и удаления собственных постов, получения ленты, лайков и подписок.
- Идентификация пользователя по заголовку `api-key`; проверка авторства при удалении поста.
- PostgreSQL и SQLAlchemy: связи между пользователями, постами, лайками, подписками и медиа, ограничения уникальности и каскадное удаление.
- Миграции Alembic, валидация данных Marshmallow и Flask-WTF.
- Описания Swagger на YAML в docstring обработчиков, Swagger UI через Flasgger.
- Интеграционные API-тесты на pytest и Flask test client с изолированной SQLite-базой.
- Логирование API и CRUD-слоя, ротация файлов ошибок.
- Docker Compose для PostgreSQL, Flask/Gunicorn и Nginx; готовый frontend обслуживается через Nginx.

## Стек

Python 3.12, Flask, Flask-RESTful, SQLAlchemy, PostgreSQL 15, Alembic, Marshmallow, Flask-WTF, Flasgger, pytest, Gunicorn, Nginx, Docker Compose.

## Архитектура

```text
Браузер -> Nginx :80 -> статические файлы dist/
                   -> /api/* -> Gunicorn :8000 -> Flask -> PostgreSQL
                   -> /media/* и Swagger -> Flask
```

Обработчики находятся в `app/api/`, операции с данными — в `app/models/crud/`, модели — в `app/models/database.py`, схемы валидации — в `app/schemas/`.

## Запуск

Из корня репозитория:

```bash
cd python_advanced_diploma
cp .env.example .env
# Настройте DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT и DB_URL в .env.
docker compose up -d --build
```

Compose подставляет имя сервиса `db` в строку подключения приложения. Миграции применяются автоматически при старте контейнера `web`. Параметры из `.env.example` предназначены для локальной разработки.

| Интерфейс | Адрес |
|---|---|
| Frontend | http://localhost |
| Swagger UI | http://localhost/apidocs/ |
| Спецификация API | http://localhost/apispec_1.json |

Для первого запроса создайте демонстрационного пользователя. В примере используются значения БД из `.env.example`; при изменении настроек замените их в команде:

```bash
docker compose exec db psql -U postgres -d twitter_db
```

```sql
INSERT INTO "user" (name, api_key) VALUES ('test_user', 'test');
```

```bash
curl http://localhost/api/users/me -H 'api-key: test'
```

Остановка: `docker compose down`. Данные PostgreSQL хранятся в томе `pgdata`, загруженные файлы — в `uploads`.

## API

| Метод | Путь | Назначение |
|---|---|---|
| GET | `/api/users/me` | Текущий пользователь |
| GET | `/api/users/<id>` | Публичный профиль |
| GET | `/api/tweets` | Лента своих постов и подписок |
| POST | `/api/tweets` | Создание поста |
| DELETE | `/api/tweets/<id>` | Удаление собственного поста |
| POST / DELETE | `/api/tweets/<id>/likes` | Лайк / отмена лайка |
| POST / DELETE | `/api/users/<id>/follow` | Подписка / отписка |
| POST | `/api/medias` | Загрузка изображения |

Защищённые маршруты принимают заголовок `api-key`. Профиль `/api/users/<id>` доступен без ключа. API не реализует самостоятельную регистрацию пользователей.

## Тестирование

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DB_URL=sqlite:// python -m pytest -q
```

На Windows установите `DB_URL` в переменные окружения перед запуском pytest. Фикстуры создают отдельную SQLite-базу для каждого теста и не используют рабочие данные PostgreSQL.

Тесты проверяют ответы API, ошибки валидации, отсутствие ключа, проверку авторства, лайки и подписки. Этот набор не заменяет проверку миграций на PostgreSQL и браузерные end-to-end тесты. Часть сценариев повторяется в нескольких тестовых файлах.

## Дальнейшее развитие

- Добавить пагинацию ленты на уровне запроса к БД.
- Усилить загрузку медиа: хранить владельца, проверять содержимое, ограничивать размер и использовать уникальные имена файлов.
- Согласовать все HTTP-коды ошибок загрузки файлов с документацией.
- Добавить проверки миграций на PostgreSQL и CI для автоматического запуска тестов.

Проект демонстрирует учебную реализацию backend и требует доработок перед эксплуатацией с реальными пользователями.
