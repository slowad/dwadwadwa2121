"""
Мини-проект: REST API для управления заметками.

Эндпоинты (CRUD):
  GET    /notes         -- список всех заметок
  GET    /notes/<id>     -- одна заметка
  POST   /notes         -- создать заметку
  PUT    /notes/<id>     -- обновить заметку целиком
  DELETE /notes/<id>     -- удалить заметку

Запуск:
  python app.py
Сервер поднимется на http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify
from database import get_connection, init_db

app = Flask(__name__)


# ---------- GET /notes : список всех заметок ----------
@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM notes ORDER BY id").fetchall()
    conn.close()
    # sqlite3.Row не сериализуется в JSON напрямую -- превращаем в dict
    notes = [dict(row) for row in rows]
    return jsonify(notes), 200


# ---------- GET /notes/<id> : одна заметка ----------
@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Заметка не найдена"}), 404

    return jsonify(dict(row)), 200


# ---------- POST /notes : создать заметку ----------
@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True)

    # Валидация входных данных -- обязательный шаг, никогда не доверяем клиенту
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Нужны поля 'title' и 'content'"}), 400

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (data["title"], data["content"]),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "title": data["title"], "content": data["content"]}), 201


# ---------- PUT /notes/<id> : обновить заметку ----------
@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    data = request.get_json(silent=True)

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Нужны поля 'title' и 'content'"}), 400

    conn = get_connection()
    existing = conn.execute("SELECT id FROM notes WHERE id = ?", (note_id,)).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": "Заметка не найдена"}), 404

    conn.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (data["title"], data["content"], note_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"id": note_id, "title": data["title"], "content": data["content"]}), 200


# ---------- DELETE /notes/<id> : удалить заметку ----------
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM notes WHERE id = ?", (note_id,)).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": "Заметка не найдена"}), 404

    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
