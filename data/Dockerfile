# Используем официальный образ Python для сборки зависимостей
FROM python:3.9-slim AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Создаем непривилегированного пользователя
RUN useradd -m appuser

# Меняем владельца файлов на непривилегированного пользователя
RUN chown -R appuser:appuser /app

# Переходим на финальный образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и файлы проекта из предыдущего этапа
COPY --from=builder /app /app

# Меняем пользователя
USER appuser

# Определяем команду для запуска приложения
CMD ["streamlit", "run", "app5.py", "--server.port=8501", "--server.address=0.0.0.0"]
