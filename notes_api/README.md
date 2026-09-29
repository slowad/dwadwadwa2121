# Notes API

Простой REST API для управления заметками. Flask + SQLite, JSON.

## Структура проекта

```
notes_api/
├── app.py            # Flask-приложение и роуты (CRUD)
├── database.py       # Подключение к SQLite и создание таблицы
├── requirements.txt  # Зависимости
└── notes.db          # База данных (создаётся автоматически при первом запуске)
```

## Запуск локально

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
python app.py
```

Сервер поднимется на `http://127.0.0.1:5000`

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | `/notes` | Список всех заметок |
| GET | `/notes/<id>` | Одна заметка по id |
| POST | `/notes` | Создать заметку |
| PUT | `/notes/<id>` | Обновить заметку |
| DELETE | `/notes/<id>` | Удалить заметку |

## Примеры запросов (curl)

**Создать заметку:**
```bash
curl -X POST http://127.0.0.1:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить хлеб", "content": "Не забыть по дороге домой"}'
```

**Получить список заметок:**
```bash
curl http://127.0.0.1:5000/notes
```

**Получить одну заметку:**
```bash
curl http://127.0.0.1:5000/notes/1
```

**Обновить заметку:**
```bash
curl -X PUT http://127.0.0.1:5000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить хлеб и молоко", "content": "Обновлённый список"}'
```

**Удалить заметку:**
```bash
curl -X DELETE http://127.0.0.1:5000/notes/1
```

## Примеры в Postman

1. Создай новую коллекцию "Notes API"
2. Добавь запрос `POST http://127.0.0.1:5000/notes`, во вкладке Body выбери `raw` → `JSON`, вставь `{"title": "...", "content": "..."}`
3. Аналогично для остальных методов, меняя тип запроса и URL

## Коды ответа

- `200 OK` — успешный GET/PUT
- `201 Created` — заметка создана
- `204 No Content` — заметка удалена
- `400 Bad Request` — не хватает полей title/content
- `404 Not Found` — заметка с таким id не найдена
