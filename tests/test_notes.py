"""
Тесты покрывают базовый CRUD для заметок и валидацию данных.

Запуск:
  python -m pytest -v
"""

import json


def test_create_note_requires_title_and_content(client):
    """Проверка валидации: при отправке неполных данных должна быть ошибка 400"""
    # Отправляем только title без content
    response = client.post("/notes", json={"title": "Заметка без содержимого"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_and_get_note(client):
    """Проверка создания заметки (POST) и последующего чтения по ID (GET)"""
    create_response = client.post(
        "/notes", json={"title": "Купить хлеб", "content": "В магазине у дома"}
    )
    assert create_response.status_code == 201
    
    data = create_response.get_json()
    assert data["title"] == "Купить хлеб"
    assert "id" in data
    note_id = data["id"]

    # Проверяем получение этой заметки
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["title"] == "Купить хлеб"


def test_get_all_notes(client):
    """Проверка получения списка всех заметок"""
    # Сначала проверяем, что база пуста
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.get_json() == []

    # Создаем две тестовые заметки
    client.post("/notes", json={"title": "Первая", "content": "Текст 1"})
    client.post("/notes", json={"title": "Вторая", "content": "Текст 2"})

    # Проверяем, что теперь возвращается список из двух элементов
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Первая"


def test_get_nonexistent_note_returns_404(client):
    """Проверка реакции сервера на запрос несуществующей заметки"""
    response = client.get("/notes/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_update_note(client):
    """Проверка обновления существующей заметки (PUT)"""
    create_response = client.post(
        "/notes", json={"title": "Старый заголовок", "content": "Старый текст"}
    )
    note_id = create_response.get_json()["id"]

    # Отправляем обновленные данные
    update_response = client.put(
        f"/notes/{note_id}", json={"title": "Новый заголовок", "content": "Новый текст"}
    )
    assert update_response.status_code == 200
    
    data = update_response.get_json()
    assert data["title"] == "Новый заголовок"
    assert data["content"] == "Новый текст"


def test_delete_note(client):
    """Проверка удаления заметки (DELETE)"""
    create_response = client.post("/notes", json={"title": "Удалить меня", "content": "Удаляемый текст"})
    note_id = create_response.get_json()["id"]

    # Удаляем заметку
    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204

    # Проверяем, что её больше нет в базе данных
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404
