# 🚀 Быстрый старт - Anomalizer v2.0

## Самый быстрый способ запустить приложение

### 🐳 Docker (рекомендуется)
```bash
# Клонирование репозитория
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer

# Запуск одной командой
docker-compose up

# Открыть в браузере: http://localhost:8505
```

### 🐍 Python venv
```bash
# Windows
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer
run.bat venv

# Linux/macOS  
git clone https://github.com/yourusername/anomalizer.git
cd anomalizer
./run.sh venv

# Открыть в браузере: http://localhost:8501
```

---

## 📋 Поддерживаемые команды запуска

| Команда | Windows | Linux/macOS | Описание |
|---------|---------|-------------|-----------|
| **venv** | `run.bat venv` | `./run.sh venv` | Python виртуальное окружение |
| **conda** | `run.bat conda` | `./run.sh conda` | Anaconda/Miniconda |
| **docker** | `run.bat docker` | `./run.sh docker` | Docker контейнер |
| **docker-prod** | `run.bat docker-prod` | `./run.sh docker-prod` | Docker + nginx |

---

## 🎯 Первое использование

1. **Загрузите тестовые данные** из папки `files_datasets/`
2. **Откройте приложение** по адресу из консоли
3. **Перетащите Excel файл** в область загрузки
4. **Выберите столбцы** для анализа
5. **Нажмите "Обнаружить аномалии"**
6. **Изучите результаты** на интерактивных графиках

---

## 🔧 Что делать если что-то не работает

### Проблемы с портами
```bash
# Если порт занят, используйте другой
streamlit run app5.py --server.port 8502
docker run -p 8507:8505 anomalizer:2.0
```

### Проблемы с Docker
```bash
# Проверка Docker
docker --version
docker-compose --version

# Пересборка
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Проблемы с Python
```bash
# Проверка Python
python --version  # Должен быть 3.8+

# Переустановка зависимостей
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 Тестовые данные

В папке `files_datasets/` доступны:
- **dataset1.xlsx** - данные с датчиков (2900+ записей)
- **dataset2.xlsx** - категориальные данные

---

## 🆘 Получить помощь

- 📖 **Полная документация**: [README.md](README.md)
- 🐛 **Сообщить об ошибке**: [GitHub Issues](https://github.com/yourusername/anomalizer/issues)
- 💬 **Обсуждения**: [GitHub Discussions](https://github.com/yourusername/anomalizer/discussions)

---

*Anomalizer v2.0 - Умное обнаружение аномалий в ваших данных* 📊