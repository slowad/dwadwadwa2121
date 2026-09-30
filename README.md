# Notes API

REST API для управления заметками с категориями, фильтрацией и пагинацией.
Итоговый проект учебной практики (блоки 1-4).

## Стек

- Python 3.11, Flask
- SQLAlchemy ORM (PostgreSQL в проде / SQLite для локальной разработки)
- pytest (тесты)
- Docker, gunicorn

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
git clone https://github.com/slowad/dwadwadwa2121.git
cd dwadwadwa2121

python -m venv .venv
.venv\Scripts\activate        # Windows

pip install -r requirements.txt
python app.py
```

Сервер поднимется на `http://127.0.0.1:5000`.

По умолчанию используется SQLite (`notes.db`). 
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


