# Dockerfile
FROM python:3.12-slim AS builder

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо requirements і встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь бекенд
COPY app.py .

# Команда запуску
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
