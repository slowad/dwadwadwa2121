# Notes API

REST API для управления заметками с категориями, фильтрацией и пагинацией.
Итоговый проект учебной практики (блоки 1-4).

**Демо:** https://ТВОЙ-АДРЕС.onrender.com

## Стек

- Python 3.11, Flask
- SQLAlchemy ORM (PostgreSQL в проде / SQLite для локальной разработки)
- pytest (тесты)
- Docker, gunicorn
- Хостинг: Render

## Структура репозитория

```
.
├── app.py            # Flask-приложение, роуты (CRUD, фильтрация, пагинация)
├── models.py         # Модели Category, Note (SQLAlchemy ORM)
├── extensions.py      # Инициализация db = SQLAlchemy()
├── conftest.py        # Фикстуры pytest
├── test_notes.py       # Тесты
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Запуск локально

```bash
git clone https://github.com/ТВОЙ-АККАУНТ/ТВОЙ-РЕПОЗИТОРИЙ.git
cd ТВОЙ-РЕПОЗИТОРИЙ

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
python app.py
```

Сервер поднимется на `http://127.0.0.1:5000`.

По умолчанию используется SQLite (`notes.db`). Для PostgreSQL задай переменную окружения:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/notes_db"
```

## Запуск через Docker

```bash
docker build -t notes-api .
docker run -p 5000:5000 notes-api
```

## Тесты

```bash
pytest -v
```

Покрытие: CRUD-операции, валидация входных данных, фильтрация по категории,
поиск по заголовку, пагинация, коды ответа (200/201/204/400/404).

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | `/categories` | Список категорий |
| POST | `/categories` | Создать категорию |
| GET | `/notes` | Список заметок (фильтры ниже) |
| GET | `/notes/<id>` | Одна заметка |
| POST | `/notes` | Создать заметку |
| PUT | `/notes/<id>` | Обновить заметку |
| DELETE | `/notes/<id>` | Удалить заметку |

**Query-параметры `/notes`:** `category_id`, `search`, `page`, `per_page`

## Примеры запросов

```bash
# Создать категорию
curl -X POST https://ТВОЙ-АДРЕС.onrender.com/categories \
  -H "Content-Type: application/json" -d '{"name": "Работа"}'

# Создать заметку
curl -X POST https://ТВОЙ-АДРЕС.onrender.com/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить хлеб", "content": "По дороге домой", "category_id": 1}'

# Список с фильтром и пагинацией
curl "https://ТВОЙ-АДРЕС.onrender.com/notes?category_id=1&page=1&per_page=10"
```

## Что можно улучшить дальше

- Аутентификация (JWT) для разграничения заметок по пользователям
- Кэширование частых запросов
- CI (GitHub Actions) для автоматического прогона тестов при пуше
