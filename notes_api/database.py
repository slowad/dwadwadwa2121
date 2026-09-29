"""
Модуль работы с базой данных.

Здесь используется "сырой" sqlite3 (без ORM) — специально, чтобы
на этом этапе было видно, что происходит на уровне SQL-запросов.
В блоке 3 заменим это на SQLAlchemy ORM.
"""

import sqlite3

DB_PATH = "notes.db"


def get_connection() -> sqlite3.Connection:
    """
    Создаёт соединение с БД.
    row_factory = sqlite3.Row позволяет обращаться к колонкам по имени
    (row["title"]), а не только по индексу (row[0]) — удобнее и надёжнее.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицу notes, если она ещё не существует."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
