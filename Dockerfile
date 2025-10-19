FROM python:3.11-slim

WORKDIR /app

# Установим нужные пакеты
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

EXPOSE 8000

# Запускаем FastAPI
CMD ["uvicorn", "src.main:f1_app.app", "--host", "0.0.0.0", "--port", "8000"]