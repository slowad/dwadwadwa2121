"""
conftest.py -- файлы с этим именем pytest подхватывает автоматически.
Здесь описаны фикстуры (fixtures) -- переиспользуемые "заготовки" для тестов.
"""

import os
import sys
import pytest

# Помогаем Python найти папку notes_api, добавляя её в пути поиска
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем готовое Flask-приложение и объект базы данных из вашего файла app.py
from notes_api.app import app as flask_app
from notes_api.app import db as _db


@pytest.fixture
def client():
    """
    Даёт тестовый клиент Flask с чистой БД для каждого теста.
    Использует базу в оперативной памяти, чтобы никогда не портить вашу рабочую notes.db.
    """
    # Переключаем Flask в режим тестирования и подменяем базу данных на виртуальную в памяти
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    # Перед тестом создаем чистые таблицы
    with flask_app.app_context():
        _db.create_all()

    # Даем тесту встроенный клиент для выполнения запросов
    with flask_app.test_client() as test_client:
        yield test_client

    # После теста полностью удаляем таблицы, чтобы тесты не влияли друг на друга
    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()
