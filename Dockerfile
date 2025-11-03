# Використовуємо Python 3.12
FROM python:3.12-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту проєкту
COPY . .

# Відкритий порт для FastAPI
EXPOSE 8000

# Команда запуску бекенду
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
