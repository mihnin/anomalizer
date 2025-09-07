#!/bin/bash

# Anomalizer v2.0 - Скрипт запуска для Linux/macOS
# Usage: ./run.sh [method]
# Methods: venv, conda, docker, docker-prod

METHOD=${1:-venv}

echo "🚀 Запуск Anomalizer v2.0"
echo "Метод: $METHOD"
echo "========================="

case $METHOD in
  "venv")
    echo "📦 Создание виртуального окружения..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
      # macOS
      python3 -m venv anomalizer-env
      source anomalizer-env/bin/activate
    else
      # Linux
      python3 -m venv anomalizer-env
      source anomalizer-env/bin/activate
    fi
    
    echo "📥 Установка зависимостей..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "🎉 Запуск приложения..."
    streamlit run app5.py
    ;;
    
  "conda")
    echo "🐍 Создание conda окружения..."
    conda create --name anomalizer-env python=3.9 -y
    conda activate anomalizer-env
    
    echo "📥 Установка зависимостей..."
    pip install -r requirements.txt
    
    echo "🎉 Запуск приложения..."
    streamlit run app5.py
    ;;
    
  "docker")
    echo "🐳 Сборка и запуск Docker контейнера..."
    docker-compose up --build
    ;;
    
  "docker-prod")
    echo "🐳 Запуск в продакшен режиме с nginx..."
    docker-compose --profile production up --build -d
    echo "✅ Приложение доступно по адресу: http://localhost"
    ;;
    
  *)
    echo "❌ Неизвестный метод: $METHOD"
    echo "Доступные методы: venv, conda, docker, docker-prod"
    exit 1
    ;;
esac