@echo off
rem Anomalizer v2.0 - Скрипт запуска для Windows
rem Usage: run.bat [method]
rem Methods: venv, conda, docker, docker-prod

set METHOD=%1
if "%METHOD%"=="" set METHOD=venv

echo 🚀 Запуск Anomalizer v2.0
echo Метод: %METHOD%
echo =========================

if "%METHOD%"=="venv" goto VENV
if "%METHOD%"=="conda" goto CONDA  
if "%METHOD%"=="docker" goto DOCKER
if "%METHOD%"=="docker-prod" goto DOCKER_PROD
goto UNKNOWN

:VENV
echo 📦 Создание виртуального окружения...
python -m venv anomalizer-env
call anomalizer-env\Scripts\activate.bat

echo 📥 Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt

echo 🎉 Запуск приложения...
streamlit run app5.py
goto END

:CONDA
echo 🐍 Создание conda окружения...
conda create --name anomalizer-env python=3.9 -y
call conda activate anomalizer-env

echo 📥 Установка зависимостей...
pip install -r requirements.txt

echo 🎉 Запуск приложения...
streamlit run app5.py
goto END

:DOCKER
echo 🐳 Сборка и запуск Docker контейнера...
docker-compose up --build
goto END

:DOCKER_PROD
echo 🐳 Запуск в продакшен режиме с nginx...
docker-compose --profile production up --build -d
echo ✅ Приложение доступно по адресу: http://localhost
goto END

:UNKNOWN
echo ❌ Неизвестный метод: %METHOD%
echo Доступные методы: venv, conda, docker, docker-prod
exit /b 1

:END