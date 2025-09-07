import pandas as pd
import numpy as np
import pytest
from anomaly_detection import calculate_stats, detect_anomalies


@pytest.fixture
def sample_data():
    """Фикстура, которая создает тестовый DataFrame."""
    data = {
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
        'value': [10, 12, 11, 100, 9],  # 100 - это очевидная аномалия
        'category': ['A', 'A', 'B', 'B', 'A']
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_data():
    """Фикстура для пустого DataFrame."""
    return pd.DataFrame({'value': []})


@pytest.fixture
def normal_data():
    """Фикстура с нормальными данными без выбросов."""
    data = {
        'value': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    }
    return pd.DataFrame(data)


@pytest.fixture
def data_with_multiple_outliers():
    """Фикстура с несколькими выбросами."""
    data = {
        'value': [10, 12, 11, 100, 9, 200, 13, -50, 15, 14],
        'category': ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'B']
    }
    return pd.DataFrame(data)


class TestCalculateStats:
    """Тесты для функции calculate_stats."""
    
    def test_calculate_stats_basic(self, sample_data):
        """Проверяем, что статистика (Q1, Q3, IQR) рассчитывается корректно."""
        iqr, q1, q3 = calculate_stats(sample_data, 'value')
        
        expected_q1 = sample_data['value'].quantile(0.25)
        expected_q3 = sample_data['value'].quantile(0.75)
        expected_iqr = expected_q3 - expected_q1

        assert iqr == expected_iqr
        assert q1 == expected_q1
        assert q3 == expected_q3
    
    def test_calculate_stats_normal_data(self, normal_data):
        """Проверяем расчет статистики для нормальных данных."""
        iqr, q1, q3 = calculate_stats(normal_data, 'value')
        
        assert q1 == 12.5
        assert q3 == 17.5
        assert iqr == 5.0
    
    def test_calculate_stats_with_nan(self):
        """Проверяем работу с NaN значениями."""
        data = pd.DataFrame({'value': [10, np.nan, 12, 13, 14, np.nan, 16]})
        iqr, q1, q3 = calculate_stats(data, 'value')
        
        # pandas по умолчанию игнорирует NaN при расчете квантилей
        assert not np.isnan(iqr)
        assert not np.isnan(q1)
        assert not np.isnan(q3)


class TestDetectAnomalies:
    """Тесты для функции detect_anomalies."""
    
    def test_detect_anomalies_basic(self, sample_data):
        """Проверяем базовое обнаружение аномалий."""
        iqr, q1, q3 = calculate_stats(sample_data, 'value')
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr

        anomalies = detect_anomalies(sample_data, 'value', lower_threshold, upper_threshold)

        assert len(anomalies) == 1
        assert anomalies.iloc[0]['value'] == 100
    
    def test_detect_anomalies_no_outliers(self, normal_data):
        """Проверяем случай без аномалий."""
        iqr, q1, q3 = calculate_stats(normal_data, 'value')
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr

        anomalies = detect_anomalies(normal_data, 'value', lower_threshold, upper_threshold)
        
        assert len(anomalies) == 0
        assert anomalies.empty
    
    def test_detect_anomalies_custom_thresholds(self, sample_data):
        """Проверяем работу с пользовательскими порогами."""
        # Устанавливаем очень узкие пороги
        lower_threshold = 10.5
        upper_threshold = 11.5
        
        anomalies = detect_anomalies(sample_data, 'value', lower_threshold, upper_threshold)
        
        # Должны найти все значения кроме 11
        assert len(anomalies) == 4
        assert 11 not in anomalies['value'].values
    
    def test_detect_anomalies_with_groups(self, sample_data):
        """Проверяем обнаружение аномалий с группировкой."""
        iqr, q1, q3 = calculate_stats(sample_data, 'value')
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr
        
        anomalies = detect_anomalies(
            sample_data, 
            'value', 
            lower_threshold, 
            upper_threshold,
            group_columns=['category']
        )
        
        # Проверяем, что аномалия найдена
        assert len(anomalies) > 0
    
    def test_detect_anomalies_with_selected_categories(self, sample_data):
        """Проверяем фильтрацию по выбранным категориям."""
        iqr, q1, q3 = calculate_stats(sample_data, 'value')
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr
        
        # Выбираем только категорию B
        anomalies = detect_anomalies(
            sample_data, 
            'value', 
            lower_threshold, 
            upper_threshold,
            group_columns=['category'],
            selected_categories={'category': ['B']}
        )
        
        # Проверяем, что найдены только аномалии категории B
        if not anomalies.empty:
            assert all(anomalies['category'] == 'B')
    
    def test_detect_anomalies_multiple_outliers(self, data_with_multiple_outliers):
        """Проверяем обнаружение нескольких аномалий."""
        iqr, q1, q3 = calculate_stats(data_with_multiple_outliers, 'value')
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr
        
        anomalies = detect_anomalies(
            data_with_multiple_outliers, 
            'value', 
            lower_threshold, 
            upper_threshold
        )
        
        # Должны найти выбросы: 100, 200, -50
        assert len(anomalies) >= 3
        assert 100 in anomalies['value'].values
        assert 200 in anomalies['value'].values
        assert -50 in anomalies['value'].values
    
    def test_detect_anomalies_empty_data(self, empty_data):
        """Проверяем работу с пустыми данными."""
        anomalies = detect_anomalies(empty_data, 'value', 0, 100)
        assert anomalies.empty
    
    def test_detect_anomalies_all_same_values(self):
        """Проверяем работу с одинаковыми значениями."""
        data = pd.DataFrame({'value': [10] * 10})
        iqr, q1, q3 = calculate_stats(data, 'value')
        
        # При всех одинаковых значениях IQR = 0
        assert iqr == 0
        
        lower_threshold = q1 - 1.5 * iqr
        upper_threshold = q3 + 1.5 * iqr
        
        anomalies = detect_anomalies(data, 'value', lower_threshold, upper_threshold)
        assert anomalies.empty


class TestEdgeCases:
    """Тесты для граничных случаев."""
    
    def test_single_value_data(self):
        """Проверяем работу с одним значением."""
        data = pd.DataFrame({'value': [42]})
        iqr, q1, q3 = calculate_stats(data, 'value')
        
        # Для одного значения все квартили равны
        assert q1 == q3 == 42
        assert iqr == 0
    
    def test_two_values_data(self):
        """Проверяем работу с двумя значениями."""
        data = pd.DataFrame({'value': [10, 20]})
        iqr, q1, q3 = calculate_stats(data, 'value')
        
        # Проверяем корректность расчета
        assert q1 <= q3
        assert iqr >= 0
    
    def test_negative_values(self):
        """Проверяем работу с отрицательными значениями."""
        data = pd.DataFrame({'value': [-100, -50, -25, -10, -5, -1, 0]})
        iqr, q1, q3 = calculate_stats(data, 'value')
        
        anomalies = detect_anomalies(data, 'value', q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        
        # Проверяем, что функция работает корректно с отрицательными числами
        assert isinstance(iqr, (int, float))
        assert isinstance(len(anomalies), int)