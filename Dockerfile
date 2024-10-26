# Используем официальный образ Python для сборки зависимостей
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт 8505
EXPOSE 8505

# Определяем команду для запуска приложения на порту 8505
CMD ["streamlit", "run", "app5.py", "--server.port=8505"]
