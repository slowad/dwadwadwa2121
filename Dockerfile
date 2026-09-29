# Базовый образ -- лёгкая версия Python 3.11
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем только requirements.txt -- если код меняется, а зависимости нет,
# Docker переиспользует закэшированный слой с pip install и не ставит всё заново
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальной код
COPY . .

# Порт, который слушает приложение внутри контейнера
EXPOSE 5000

# gunicorn -- "боевой" WSGI-сервер (в отличие от app.run(), который только для разработки)
# app:app -- означает "в файле app.py возьми объект app"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
