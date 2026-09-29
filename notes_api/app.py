from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Настраиваем путь к локальному файлу базы данных notes.db
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "notes.db")

# Указываем SQLAlchemy использовать SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем ORM
db = SQLAlchemy(app)

# Создаем модель таблицы в виде класса Python (Requirement Блока 3)
class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Переводим объект базы данных в обычный словарь для JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# ---------- GET /notes : получить все заметки ----------
@app.route("/notes", methods=["GET"])
def get_notes():
    # ORM сама делает SQL-запрос SELECT * FROM notes
    notes_list = Note.query.order_by(Note.id).all()
    return jsonify([note.to_dict() for note in notes_list]), 200

# ---------- GET /notes/<id> : одна заметка ----------
@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id: int):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify({"error": "Заметка не найдена"}), 404
    return jsonify(note.to_dict()), 200

# ---------- POST /notes : создать заметку ----------
@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True)
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Нужны поля 'title' и 'content'"}), 400

    # Создаем объект нашей модели (строку таблицы)
    new_note = Note(title=data["title"], content=data["content"])
    db.session.add(new_note)  # Добавляем в сессию
    db.session.commit()       # Сохраняем в файл базы данных

    return jsonify(new_note.to_dict()), 201

# ---------- PUT /notes/<id> : обновить заметку ----------
@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    data = request.get_json(silent=True)
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Нужны поля 'title' и 'content'"}), 400

    note = Note.query.get(note_id)
    if note is None:
        return jsonify({"error": "Заметка не найдена"}), 404

    note.title = data["title"]
    note.content = data["content"]
    db.session.commit()

    return jsonify(note.to_dict()), 200

# ---------- DELETE /notes/<id> : удалить заметку ----------
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    note = Note.query.get(note_id)
    if note is None:
        return jsonify({"error": "Заметка не найдена"}), 404

    db.session.delete(note)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    # Автоматически создаем таблицы внутри файла notes.db при старте
    with app.app_context():
        db.create_all()
    app.run(debug=True)
