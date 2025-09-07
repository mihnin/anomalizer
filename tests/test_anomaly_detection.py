import pandas as pd
import pytest
from anomaly_detection import calculate_stats, detect_anomalies

# Создаем тестовые данные один раз для всех тестов в этом файле
@pytest.fixture
def sample_data():
    """Фикстура, которая создает тестовый DataFrame."""
    data = {
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
        'value': [10, 12, 11, 100, 9] # 100 - это очевидная аномалия
    }
    return pd.DataFrame(data)

# Тест для функции calculate_stats
def test_calculate_stats(sample_data):
    """Проверяем, что статистика (Q1, Q3, IQR) рассчитывается корректно."""
    iqr, q1, q3 = calculate_stats(sample_data, 'value')
    
    # Для данных [9, 10, 11, 12, 100]
    # Q1 будет 9.5, Q3 будет 18.5, IQR будет 9.0
    # pd.quantile может дать немного другие результаты в зависимости от интерполяции
    # Давайте проверим это с помощью pandas
    expected_q1 = sample_data['value'].quantile(0.25)
    expected_q3 = sample_data['value'].quantile(0.75)
    expected_iqr = expected_q3 - expected_q1

    assert iqr == expected_iqr
    assert q1 == expected_q1
    assert q3 == expected_q3

# Тест для функции detect_anomalies
def test_detect_anomalies(sample_data):
    """Проверяем, что функция правильно находит аномалии."""
    # Рассчитываем пороги на основе IQR
    iqr, q1, q3 = calculate_stats(sample_data, 'value')
    lower_threshold = q1 - 1.5 * iqr
    upper_threshold = q3 + 1.5 * iqr

    # Находим аномалии
    anomalies = detect_anomalies(sample_data, 'value', lower_threshold, upper_threshold)

    # Проверяем, что была найдена ровно одна аномалия
    assert len(anomalies) == 1
    # Проверяем, что значение этой аномалии - 100
    assert anomalies.iloc[0]['value'] == 100