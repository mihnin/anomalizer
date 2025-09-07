"""
Модуль для управления версией приложения Anomalizer.
"""

import os
from pathlib import Path


def get_version() -> str:
    """
    Получает текущую версию приложения из файла VERSION.
    
    Returns:
        Строка с номером версии
    """
    try:
        version_file = Path(__file__).parent / "VERSION"
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "2.0"  # Fallback версия


__version__ = get_version()

# Информация о версии
VERSION_INFO = {
    'version': __version__,
    'name': 'Anomalizer',
    'description': 'Инструмент для обнаружения аномалий в данных',
    'author': 'Anomalizer Team',
    'features': [
        'Обнаружение аномалий методом IQR',
        'Интерактивная визуализация',
        'Поддержка группировки данных',
        'Экспорт результатов в Excel',
        'Анализ всех числовых столбцов'
    ]
}